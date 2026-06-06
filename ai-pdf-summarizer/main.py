from pathlib import Path

import requests
from pypdf import PdfReader

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text=""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text = text+page_text + "\n"
    
    return text

def summarize_text(text):
    prompt = f""" You are an AI assistant.

Summarize the following PDF content in simple English.

Return the answer in Markdown format with these sections:

# Summary
# Key Points
# Important Terms
# Final Takeaway

PDF Content:
{text[:12000]}
"""
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        },
        timeout=300
    )

    data = response.json()
    return data["response"]

def save_summary(summary,file_name):
    Path("output").mkdir(exist_ok=True)

    output_file_name = Path(file_name).stem + "_summary.md"
    output_path = Path("output") / output_file_name

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(summary)

    return output_path

def main():
    print("Reading PDF...")
    file_name = "Interactive Text-to-Image Retrieval with Large Language Models.pdf"
    text = extract_text_from_pdf(file_name)

    if not text.strip():
        print("No text found in PDF.")
        return
    
    print("Summarizing...")
    summary = summarize_text(text)

    save_summary(summary,file_name)

    print("Done! Check output/summary.md")

if __name__ == "__main__":
    main()