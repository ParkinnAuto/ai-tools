import { GoogleGenAI } from "@google/genai";
import { NextResponse } from "next/server";

const ai = new GoogleGenAI({
  apiKey: process.env.GEMINI_API_KEY,
});

export async function POST(request: Request) {
  try {
    // รับข้อมูลที่ TalkButton ส่งมา
    const body = await request.json();

    const message = body.message;
    const language = body.language;

    if (!message) {
      return NextResponse.json(
        { error: "Message is required" },
        { status: 400 }
      );
    }

    // ส่งข้อความไปให้ Gemini
    const response = await ai.interactions.create({
      model: "gemini-3.5-flash-lite",
      input: `
You are a friendly AI robot assistant.

Answer briefly and naturally.

Do not answer with emojis.

Answer fast

Reply using this language code:
${language}

User says:
${message}
      `,
    });

    // ส่งคำตอบกลับไปให้ TalkButton
    return NextResponse.json({
      reply: response.output_text,
    });

  } catch (error) {
    console.error("Gemini API Error:", error);

    return NextResponse.json(
      { error: "Failed to get Gemini response" },
      { status: 500 }
    );
  }
}