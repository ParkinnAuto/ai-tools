AI Multi-PDF Summarizer

An upgraded version of the PDF summarizer that supports multiple PDF files.

Features

Read all PDF files from an input folder
Summarize each PDF automatically
Save each summary as a separate Markdown file
Generate output files based on the original PDF names
Run locally using Ollama

Tech Stack

Python
pypdf
requests
Ollama
Qwen2.5
Why I Built This

I built these projects to learn how to integrate existing AI models into practical tools.
The goal is to understand how AI applications work by building small, useful projects step by step.

How to Run

Each project has its own folder and setup instructions.

Example:

cd ai-multi-pdf-summarizer
pip install -r requirements.txt
python main.py

Make sure Ollama is installed and the model is available:

ollama pull qwen2.5:1.5b
Notes
PDF files are ignored and should not be uploaded to GitHub.
Virtual environments are ignored.
Generated summaries can be included as examples if they do not contain private or copyrighted content.