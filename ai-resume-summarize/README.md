# CKQ - AI Resume Screening Assistant

CKQ is a simple cross-platform AI resume screening assistant designed to help HR users quickly analyze resumes and CVs.

The application allows users to upload a resume file, extract its content, and generate a structured HR-focused summary using an external AI API. It is built as a personal learning project to practice full-stack development, AI API integration, file upload handling, and cross-platform application development.
URL to website: ckq-resume.vercel.app
---

## Overview

CKQ helps convert resume documents into structured candidate insights, including:

- Candidate summary
- Key skills
- Work experience
- Education
- Strengths
- Concerns or missing information
- Recommended roles
- HR recommendation
- English summary
- Chinese summary

This project is intended for educational and personal portfolio purposes.

---

## Features

- Upload resume or CV files
- Support for PDF, DOCX, and TXT files
- Extract text from uploaded documents
- Clean extracted resume text before analysis
- Analyze resumes using Groq AI API
- Return structured JSON results
- Minimal and modern React Native UI
- White and purple SaaS-style design
- Works on web through Expo
- Backend separated from AI service for cleaner architecture

---

## Tech Stack

### Frontend

- React Native
- Expo
- Expo Router
- TypeScript
- Axios
- Expo Document Picker

### Backend

- Node.js
- Express.js
- TypeScript
- Multer
- Axios
- CORS
- dotenv

### AI Service

- Python
- FastAPI
- Uvicorn
- pypdf
- python-docx
- python-dotenv
- requests
- Groq API

---

## Project Structure

```txt
ai-resume-summarize/
│
├── client/
│   ├── src/
│   │   ├── app/
│   │   │   ├── _layout.tsx
│   │   │   └── index.tsx
│   │   │
│   │   ├── components/
│   │   │   ├── UploadBox.tsx
│   │   │   └── ResultCard.tsx
│   │   │
│   │   └── services/
│   │       └── api.ts
│   │
│   ├── app.json
│   └── package.json
│
├── server/
│   ├── src/
│   │   ├── config/
│   │   ├── controllers/
│   │   │   └── analyzeController.ts
│   │   ├── middleware/
│   │   │   └── uploadMiddleware.ts
│   │   ├── routes/
│   │   │   └── analyzeRoutes.ts
│   │   └── server.ts
│   │
│   └── package.json
│
├── ai-service/
│   ├── main.py
│   ├── extract_text.py
│   ├── analyze_resume.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
