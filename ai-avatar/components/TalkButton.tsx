"use client";

import { useState } from "react";

// ผลลัพธ์ที่ Speech Recognition ส่งกลับ
interface SpeechRecognitionEvent extends Event {
  results: {
    [index: number]: {
      [index: number]: {
        transcript: string;
      };
    };
  };
}

// ตัว recognition ที่เราใช้งาน
interface SpeechRecognitionInstance {
  lang: string;
  onresult: ((event: SpeechRecognitionEvent) => void) | null;
  onend: (() => void) | null;
  start: () => void;
}

// constructor สำหรับสร้าง recognition
interface SpeechRecognitionConstructor {
  new (): SpeechRecognitionInstance;
}

const TalkButton = () => {
  const [text, setText] = useState("");
  const [language, setLanguage] = useState("th-TH");
  const [isListening, setIsListening] = useState(false);

  // อ่านข้อความออกเสียง
  const speakText = (message: string) => {
    if (!("speechSynthesis" in window)) {
      console.log("Speech synthesis not supported");
      return;
    }

    // ยกเลิกเสียงเก่าก่อน
    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(message);

    speech.lang = language;
    speech.volume = 1;
    speech.rate = 1;
    speech.pitch = 1;

    // มือถือบางเครื่องต้องหน่วงนิดหนึ่ง
    setTimeout(() => {
      window.speechSynthesis.speak(speech);
    }, 150);
  };

  const startListening = () => {
    const speechWindow = window as typeof window & {
      SpeechRecognition?: SpeechRecognitionConstructor;
      webkitSpeechRecognition?: SpeechRecognitionConstructor;
    };

    const SpeechRecognition =
      speechWindow.SpeechRecognition ||
      speechWindow.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Browser นี้ไม่รองรับ Speech Recognition");
      return;
    }

    /*
      ปลุกระบบเสียงจาก user gesture โดยตรง
      ช่วยให้มือถืออนุญาต speechSynthesis ได้ง่ายขึ้น
    */
    const unlockSpeech = new SpeechSynthesisUtterance("");
    window.speechSynthesis.speak(unlockSpeech);

    const recognition = new SpeechRecognition();

    recognition.lang = language;

    setIsListening(true);

    recognition.onresult = async (event) => {
      const transcript = event.results[0][0].transcript;

      setText(transcript);
      console.log("You said:", transcript);

      try {
        // ส่งข้อความไปให้ Gemini
        const response = await fetch("/api/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: transcript,
            language: language,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          console.error("API Error:", data);
          setText("AI error");
          return;
        }

        // แสดงคำตอบ AI
        setText(data.reply);
        console.log("AI:", data.reply);

        // อ่านคำตอบออกเสียง
        speakText(data.reply);

      } catch (error) {
        console.error("Fetch error:", error);
        setText("Connection error");
      }
    };

    // หยุดฟังแล้วให้ปุ่มกลับสีเดิม
    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  return (
    <div className="flex w-full max-w-2xl flex-col gap-3 rounded-2xl border border-slate-700/70 bg-slate-900/90 p-3 shadow-2xl md:flex-row md:items-center">

      {/* เลือกภาษา */}
      <select
        value={language}
        onChange={(event) => setLanguage(event.target.value)}
        className="h-12 rounded-xl border border-slate-700 bg-slate-950 px-4 text-sm font-medium text-white outline-none focus:border-cyan-400"
      >
        <option value="th-TH">🇹🇭 ไทย</option>
        <option value="en-US">🇺🇸 English</option>
        <option value="zh-CN">🇨🇳 中文</option>
        <option value="lo-LA">🇱🇦 ລາວ</option>
        <option value="es-ES">🇪🇸 Español</option>
      </select>

      {/* ปุ่มเริ่มฟัง */}
      <button
        onClick={startListening}
        disabled={isListening}
        className={`
          h-12 rounded-xl px-7 font-semibold transition active:scale-95
          ${
            isListening
              ? "bg-red-500 text-white"
              : "bg-cyan-500 text-slate-950 hover:bg-cyan-400"
          }
        `}
      >
        {isListening ? "🎙️ Listening..." : "🎤 Talk"}
      </button>

      {/* แสดงข้อความ */}
      <div className="min-h-12 flex-1 rounded-xl bg-slate-950/70 px-4 py-3 text-sm text-slate-300">
        {text || "Your speech will appear here..."}
      </div>
    </div>
  );
};

export default TalkButton;