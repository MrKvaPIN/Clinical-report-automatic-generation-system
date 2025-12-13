# Clinical-report-automatic-generation-system

A lightweight web application built with Flask. It calls the DeepSeek large language model to perform structured parsing of input medical records and generate clinical reports. The system supports Markdown rendering, code highlighting, and basic XSS sanitization.

## Key Features
- Paste raw medical record text and automatically generate a structured clinical report (patient basics, diagnosis and pathology, treatment course and response, prognosis assessment and follow-up plan)
- Front-end renders model responses with Markdown and code highlighting for improved readability
- Back-end provides a unified wrapper for calling the DeepSeek Chat Completions API

## Tech Stack
- Back end: `Python 3`, `Flask`, `requests`
- Front end: vanilla `HTML/CSS/JS`, `marked` (Markdown parsing), `DOMPurify` (XSS sanitization), `highlight.js` (code highlighting)

## Project Structure
```text
Clinical-report-automatic-generation-system-main/
├─ deepseek_api.py           # Flask app and DeepSeek API wrapper
├─ templates/
│  └─ index.html            # Front-end page (chat UI and rendering)
├─ static/
│  └─ style.css             # Page styles
└─ Document recognition results/             # Sample data and outputs (not required to run)
