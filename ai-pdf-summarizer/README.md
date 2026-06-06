# AI PDF Summarizer

A simple AI-powered PDF summarizer that extracts text from PDF files and summarizes the content using a local LLM through Ollama.

## Features

- Extract text from PDF files
- Summarize PDF content using Ollama
- Generate Markdown summary files
- Run locally without API keys
- No paid AI API required

## Tech Stack

- Python
- pypdf
- requests
- Ollama
- Qwen2.5 1.5B

## How It Works

1. Read PDF file
2. Extract text from pages
3. Send text to Ollama local API
4. Generate summary
5. Save result as Markdown

## Setup

```bash
pip install -r requirements.txt

Install Ollama and pull the model: ollama pull qwen2.5:1.5b

Run the project: python main.py

Output: The summary will be saved in the output/ folder.