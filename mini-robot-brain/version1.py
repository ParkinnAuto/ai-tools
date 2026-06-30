import os
import shutil
import queue
import threading
import asyncio

import imageio_ffmpeg
import cv2
import requests
import sounddevice as sd
import edge_tts
from playsound import playsound
from scipy.io.wavfile import write
import whisper


# =========================
# 1. Setup FFmpeg for Whisper
# =========================

ffmpeg_source = imageio_ffmpeg.get_ffmpeg_exe()
ffmpeg_dir = os.path.dirname(ffmpeg_source)
ffmpeg_target = os.path.join(ffmpeg_dir, "ffmpeg.exe")

if not os.path.exists(ffmpeg_target):
    shutil.copy(ffmpeg_source, ffmpeg_target)

os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]


# =========================
# 2. Settings
# =========================

OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "qwen2.5:1.5b"

CAMERA_INDEX = 0

RECORD_SECONDS = 3
SAMPLE_RATE = 16000

RECORDINGS_DIR = "recordings"
CAPTURES_DIR = "captures"
TEMP_AUDIO_DIR = "temp_audio"

AUDIO_PATH = os.path.join(RECORDINGS_DIR, "voice.wav")
IMAGE_PATH = os.path.join(CAPTURES_DIR, "latest.jpg")


# =========================
# 3. Text-to-Speech
# =========================

def choose_voice(language):
    if language == "thai":
        return "th-TH-PremwadeeNeural"

    if language == "chinese":
        return "zh-CN-XiaoxiaoNeural"

    if language == "spanish":
        return "es-MX-DaliaNeural"

    return "en-US-AriaNeural"


async def speak_async(text, language="thai"):
    os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

    voice = choose_voice(language)
    audio_file = os.path.join(TEMP_AUDIO_DIR, "answer.mp3")

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(audio_file)

    playsound(audio_file)

    if os.path.exists(audio_file):
        os.remove(audio_file)


def speak(text, language="thai"):
    print(f"\nAI: {text}\n")
    asyncio.run(speak_async(text, language))


# =========================
# 4. Speech-to-Text
# =========================

def record_audio():
    print("\nListening... Speak now.")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    write(AUDIO_PATH, SAMPLE_RATE, audio)

    print("Recording finished")


def transcribe_audio(whisper_model):
    print("Transcribing...")

    try:
        result = whisper_model.transcribe(
            AUDIO_PATH,
            fp16=False
        )

        text = result["text"].strip()
        return text

    except Exception as error:
        print("Whisper error:", error)
        return ""


# =========================
# 5. Ask Ollama
# =========================

def ask_ollama(user_text, language="thai"):
    if language == "thai":
        answer_language = "Thai"
    elif language == "chinese":
        answer_language = "Mandarin Chinese"
    elif language == "spanish":
        answer_language = "Spanish"
    else:
        answer_language = "English"

    prompt = f"""
You are a cute mini robot brain assistant language teacher.

Rules:
- Answer in {answer_language}.
- You can only answer in Thai, English, Mandarin Chinese, or Spanish.
- Do not answer in Japanese.
- Keep the answer short.
- Answer in 1 or 2 sentences.
- Answer and helping user learning new language
- Help user fix incorrect sentence

User said:
{user_text}

Answer:
"""

    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.5,
            "num_predict": 120
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        data = response.json()
        answer = data.get("response", "").strip()

        if not answer:
            return "ขอโทษครับ ผมยังตอบไม่ได้ตอนนี้"

        return answer

    except Exception as error:
        print("Ollama error:", error)
        return "ขอโทษครับ ผมเชื่อมต่อ Ollama ไม่ได้"


# =========================
# 6. Detect Language
# =========================

def detect_language(text):
    # Thai
    if any("\u0E00" <= char <= "\u0E7F" for char in text):
        return "thai"

    # Chinese
    if any("\u4E00" <= char <= "\u9FFF" for char in text):
        return "chinese"

    # Default
    return "english"


# =========================
# 7. Camera
# =========================

def camera_loop(command_queue, stop_event):
    camera = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

    if not camera.isOpened():
        print("Cannot open camera")
        stop_event.set()
        return

    window_name = "Mini Robot Brain"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    print("Camera started.")
    print("Press V = talk")
    print("Press C = capture")
    print("Press Q = quit")

    while not stop_event.is_set():
        success, frame = camera.read()

        if not success:
            print("Cannot read camera")
            break

        cv2.putText(
            frame,
            "Mini Robot Brain",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "V: Talk | C: Capture | Q: Quit",
            (20, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("v") or key == ord("V"):
            cv2.imwrite(IMAGE_PATH, frame)
            command_queue.put("talk")

        elif key == ord("c") or key == ord("C"):
            cv2.imwrite(IMAGE_PATH, frame)
            print("Image saved:", IMAGE_PATH)

        elif key == ord("q") or key == ord("Q") or key == 27:
            stop_event.set()
            break

    camera.release()
    cv2.destroyAllWindows()


# =========================
# 8. Main Program
# =========================

def main():
    os.makedirs(RECORDINGS_DIR, exist_ok=True)
    os.makedirs(CAPTURES_DIR, exist_ok=True)
    os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

    print("Loading Whisper model...")
    whisper_model = whisper.load_model("tiny")
    print("Whisper model loaded.")

    command_queue = queue.Queue()
    stop_event = threading.Event()

    camera_thread = threading.Thread(
        target=camera_loop,
        args=(command_queue, stop_event),
        daemon=True
    )

    camera_thread.start()

    speak(
        "สวัสดีครับ ผมคือมินิโรบอตเบรน กดปุ่ม V แล้วพูดกับผมได้เลย",
        language="thai"
    )

    while not stop_event.is_set():
        try:
            command = command_queue.get(timeout=0.1)
        except queue.Empty:
            continue

        if command == "talk":
            record_audio()

            user_text = transcribe_audio(whisper_model)

            if not user_text:
                speak("ผมฟังไม่ชัดครับ ลองพูดใหม่อีกครั้ง", language="thai")
                continue

            print("\nYou:", user_text)

            language = detect_language(user_text)
            print("Language:", language)

            answer = ask_ollama(user_text, language)

            speak(answer, language)


if __name__ == "__main__":
    main()