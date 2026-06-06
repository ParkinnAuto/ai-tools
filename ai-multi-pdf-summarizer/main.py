from pathlib import Path

import requests
from pypdf import PdfReader

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"

INPUT_FOLDER = Path("input")
OUTPUT_FOLDER = Path("output")

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    max_pages = min(10, len(reader.pages))

    for i in range(max_pages):
        print(f"Reading page {i + 1}...")

        page = reader.pages[i]
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

def summarize_text(text):
    prompt = f"""
You are an AI assistant.

Summarize the following PDF content in simple English.

Return the answer in Markdown format with these sections:

# Summary
# Key Points
# Important Terms
# Final Takeaway

PDF Content:
{text[:10000]}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        },
        timeout=300,
    )

    response.raise_for_status()
    data = response.json()

    return data["response"]

def save_summary(summary, pdf_path):
    OUTPUT_FOLDER.mkdir(exist_ok=True)

    output_file_name = pdf_path.stem + "_summary.md"
    output_path = OUTPUT_FOLDER / output_file_name

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(summary)
    
    return output_path

def summarize_pdf(pdf_path):
    print(f"\nProcessing: {pdf_path.name}")

    text = extract_text_from_pdf(pdf_path)

    if not text.strip():
        print("No text found. Skipping this file.")
        return
    
    print("Summarizing...")
    summary = summarize_text(text)

    output_path = save_summary(summary, pdf_path)

    print(f"  Done: {output_path}")

def main():
    if not INPUT_FOLDER.exists():
        INPUT_FOLDER.mkdir()
        print("Created input folder. Please add PDF files into input/.")
        return
    
    pdf_files = list(INPUT_FOLDER.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in this input folder.")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s).")

    for pdf_path in pdf_files:
        summarize_pdf(pdf_path)
    
    print("\nAll done!")

if __name__ == "__main__":
    main()