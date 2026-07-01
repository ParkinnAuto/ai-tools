from pypdf import PdfReader
from docx import Document
import os
import re

def clean_extracted_text(text: str) -> str:
    text = re.sub(r'(?<=\b[A-Za-z])\s(?=[A-Za-z]\b)', '', text)

    text = re.sub(r'[ \t]+', ' ', text)

    text = re.sub(r'\n\s*\n+', '\n\n', text)

    return text.strip()

def extract_text_from_pdf(file_path:str) -> str:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text = text + page_text + "\n"
    
    return text

def extract_text_from_docx(file_path:str) -> str:
    document = Document(file_path)
    text = ""

    for paragraph in document.paragraphs:
        text = text + paragraph.text + "\n"
    
    return text

def extract_text_from_txt(file_path:str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def extract_text(file_path:str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)

    elif ext == ".docx":
        text = extract_text_from_docx(file_path)

    elif ext == ".txt":
        text = extract_text_from_txt(file_path)
    
    else:
        raise ValueError("Unsupported file type. Please upload PDF, DOCX, or TXT.")

    return clean_extracted_text(text)
