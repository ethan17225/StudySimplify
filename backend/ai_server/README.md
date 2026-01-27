# Backend — AI Server

Overview
- This folder contains the AI backend server used by the StudySimplify project. It exposes endpoints for uploading documents and generating summaries, quizzes, and flashcards using Groq/LLM integrations.

Prerequisites
- Python 3.10+ recommended
- pip
- A GROQ API key (set in `.env` as `GROQ_API_KEY`)

Install and setup
1. From the project root, create and activate a virtual environment (macOS/Linux):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies from the project `requirements.txt` in the repo root:

```bash
pip install -r ../../requirements.txt
```

3. Create a `.env` file in `backend/ai_server` with your environment variables:

```bash
# backend/ai_server/.env
GROQ_API_KEY=your_groq_api_key_here
```

Run the server
- From `backend/ai_server` run (reload enabled for development):

```bash
uvicorn app:app --reload --port 8080
```

- Or run directly with Python (the module starts uvicorn when executed):

```bash
python app.py
```

API endpoints
- POST /process_file
  - Description: Upload a PDF or DOCX file; server extracts text and stores it in memory.
  - Form field: `file` (multipart/form-data)
  - Example:

```bash
curl -X POST "http://localhost:8080/process_file" -F "file=@/path/to/document.pdf"
```

- POST /process_text
  - Description: Process the previously uploaded file content with one of the functions: `summarize`, `quiz`, `flashcards`.
  - Body: JSON `{ "function": "summarize" }` (Content-Type: application/json)
  - Example:

```bash
curl -X POST "http://localhost:8080/process_text" -H "Content-Type: application/json" \
  -d '{"function":"summarize"}'
```

Notes & security
- Supported file types: PDF and DOCX.
- The server stores the uploaded document text in a global variable `file_content` (in-memory). This is not suitable for concurrent multi-user production use—consider per-request processing or persistent storage.
- There is a hardcoded Groq API key present in `backend/ai_server/utils/summarize_text.py`. Replace it with reading from the `.env` file and remove the hardcoded secret immediately.

Dependencies
- Python dependencies are listed at the repo root in [requirements.txt](../requirements.txt).
- Frontend dependencies live in [frontend/study-assistance-ui/package.json](../frontend/study-assistance-ui/package.json).

Troubleshooting
- If imports fail, ensure you're using the virtual environment and installed the required packages.
- If the LLM calls fail, verify `GROQ_API_KEY` is set and valid.

Maintainers
- Backend: `backend/ai_server/app.py` and `backend/ai_server/utils/*`.

