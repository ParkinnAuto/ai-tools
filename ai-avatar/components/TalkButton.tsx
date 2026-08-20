"use client";

import { useState } from "react";

// Type ของผลลัพธ์จาก Speech Recognition
interface SpeechRecognitionEvent extends Event {
  results: {
    [index: number]: {
      [index: number]: {
        transcript: string;
      };
    };
  };
}

// Type ของตัว recognition
interface SpeechRecognitionInstance {
  lang: string;
  onresult: ((event: SpeechRecognitionEvent) => void) | null;
  onend: (() => void) | null;
  start: () => void;
}

// Type ของ constructor
interface SpeechRecognitionConstructor {
  new (): SpeechRecognitionInstance;
}

const TalkButton = () => {
  // เก็บข้อความที่พูด / AI ตอบ
  const [text, setText] = useState("");

  // เก็บภาษาที่เลือก
  const [language, setLanguage] = useState("th-TH");

  // เช็กว่าตอนนี้กำลังฟังเสียงอยู่ไหม
  const [isListening, setIsListening] = useState(false);

  const startListening = () => {
    // รองรับทั้ง SpeechRecognition และ webkitSpeechRecognition
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

    // สร้างตัวรับเสียง
    const recognition = new SpeechRecognition();

    // ใช้ภาษาที่ user เลือก
    recognition.lang = language;

    // เปลี่ยนสถานะเป็นกำลังฟัง
    setIsListening(true);

    // เมื่อ browser แปลงเสียงเป็นข้อความเสร็จ
    recognition.onresult = async (event) => {
      const transcript = event.results[0][0].transcript;

      setText(transcript);
      console.log("You said:", transcript);

      try {
        // ส่งข้อความไป Next.js API
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
        console.log("AI:", data.reply);
        setText(data.reply);

        // อ่านคำตอบ AI ออกเสียง
        const speech = new SpeechSynthesisUtterance(data.reply);
        speech.lang = language;

        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(speech);
      } catch (error) {
        console.error("Fetch error:", error);
        setText("Connection error");
      }
    };

    // เมื่อหยุดฟัง ไม่ว่าจะได้ข้อความหรือไม่
    recognition.onend = () => {
      setIsListening(false);
    };

    // เริ่มฟังไมค์
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

      {/* ปุ่มฟังเสียง */}
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