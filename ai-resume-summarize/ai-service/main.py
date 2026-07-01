from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os

from extract_text import extract_text
from analyze_resume import analyze_resume

app = FastAPI()

UPLOAD_DIR = "uplaods"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {
        "message": "CKQ AI service is running"
    }

@app.post("/analyze")
async def analyze_uploaded_resume(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        resume_text = extract_text(file_path)

        analysis_result = analyze_resume(resume_text)

        return {
            "message": "Resume analyzed successfully",
            "filename": file.filename,
            "textLength": len(resume_text),
            "extractedTextPreview": resume_text[:1000],
            "analysis": analysis_result
        }

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Failed to analyze resume",
                "error": str(error)
            }
        )