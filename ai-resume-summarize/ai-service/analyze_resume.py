import os
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

MODEL_NAME = "llama-3.1-8b-instant"


def ensure_complete_result(result: dict) -> dict:
    default_result = {
        "candidate_summary": "",
        "key_skills": [],
        "work_experience": [],
        "education": [],
        "strengths": [],
        "concerns_or_missing_info": [],
        "recommended_roles": [],
        "hr_recommendation": "",
        "english_summary": "",
        "chinese_summary": ""
    }

    for key, default_value in default_result.items():
        if key not in result:
            result[key] = default_value

    return result


def clean_ai_json_response(ai_text: str) -> str:
    """
    Clean AI response before parsing JSON.
    This helps when the model returns markdown or invalid escape characters.
    """

    # Remove markdown json block if exists
    ai_text = ai_text.strip()
    ai_text = ai_text.replace("```json", "")
    ai_text = ai_text.replace("```", "")
    ai_text = ai_text.strip()

    # Extract only JSON object between first { and last }
    start = ai_text.find("{")
    end = ai_text.rfind("}")

    if start != -1 and end != -1:
        ai_text = ai_text[start:end + 1]

    # Remove invalid backslashes such as \学, \生
    # Keep valid JSON escapes like \n, \", \\, \uXXXX
    ai_text = re.sub(r'\\(?!["\\/bfnrtu])', '', ai_text)

    return ai_text


def analyze_resume(resume_text: str) -> dict:
    if not resume_text or len(resume_text.strip()) == 0:
        return {
            "candidate_summary": "No readable text found in the uploaded resume.",
            "key_skills": [],
            "work_experience": [],
            "education": [],
            "strengths": [],
            "concerns_or_missing_info": [],
            "recommended_roles": [],
            "hr_recommendation": "Unable to analyze because the resume text is empty.",
            "english_summary": "",
            "chinese_summary": ""
        }

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing. Please check your .env file.")

    prompt = f"""
You are an HR resume screening assistant.

Analyze the resume text below and return ONLY valid JSON.

Important rules:
- Return valid JSON only.
- Do not include markdown.
- Do not include explanations outside JSON.
- You must include ALL fields.
- Do not remove any field.
- If information is missing, return "" or [].
- Do not use backslashes in normal text.
- chinese_summary must be Simplified Chinese only.
- chinese_summary must be short, clear, and no longer than 3 sentences.
- english_summary must be no longer than 3 sentences.
- strengths must contain 3 to 5 items.
- concerns_or_missing_info must contain 2 to 4 items.
- hr_recommendation must be a clear hiring recommendation for HR.

Return exactly this JSON structure:

{{
  "candidate_summary": "",
  "key_skills": [],
  "work_experience": [],
  "education": [],
  "strengths": [],
  "concerns_or_missing_info": [],
  "recommended_roles": [],
  "hr_recommendation": "",
  "english_summary": "",
  "chinese_summary": ""
}}

Resume text:
\"\"\"
{resume_text[:10000]}
\"\"\"
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": "You are a professional HR resume screening assistant. Return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1,
        "max_tokens": 1800,
        "response_format": {
            "type": "json_object"
        }
    }

    response = requests.post(
        GROQ_API_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(f"Groq API error: {response.text}")

    ai_text = response.json()["choices"][0]["message"]["content"]

    try:
        cleaned_ai_text = clean_ai_json_response(ai_text)
        result = json.loads(cleaned_ai_text)
        return ensure_complete_result(result)

    except json.JSONDecodeError:
        return {
            "candidate_summary": "",
            "key_skills": [],
            "work_experience": [],
            "education": [],
            "strengths": [],
            "concerns_or_missing_info": [],
            "recommended_roles": [],
            "hr_recommendation": "",
            "english_summary": "",
            "chinese_summary": "",
            "raw_ai_response": ai_text,
            "warning": "AI response was not valid JSON."
        }