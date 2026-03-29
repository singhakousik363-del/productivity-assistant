# Multi-Agent Productivity Assistant

A multi-agent AI system built with Google Gemini that helps you manage tasks, schedules, and notes.

---

## How it works

```
You (user)
    ↓
Primary Agent (Gemini decides what you want)
    ↓
Task Agent | Calendar Agent | Notes Agent
    ↓
SQLite Database
    ↓
FastAPI (HTTP API)
```

---

## Setup (step by step)

### 1. Install Python
Download from https://python.org — version 3.10 or higher.

### 2. Get your Gemini API key
- Go to https://aistudio.google.com
- Click "Get API Key"
- Copy the key

### 3. Set up the project
Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux):

```bash
# Go into the project folder
cd productivity-assistant

# Install all dependencies
pip install -r requirements.txt
```

### 4. Add your API key
Open the `.env` file and replace `your_api_key_here` with your actual key:

```
GEMINI_API_KEY=AIzaSy...your_real_key_here
```

---

## Running the project

### Option A — Test in terminal (quickest way to try it)
```bash
python agents/primary_agent.py
```
Then type messages like:
- `Add task Buy groceries`
- `Schedule meeting on 2026-04-10 at 14:00`
- `Save note: Ideas | Launch campaign in May`
- `List tasks`

### Option B — Run as an API server
```bash
uvicorn api.main:app --reload
```
Then open http://localhost:8000 in your browser.

Visit http://localhost:8000/docs to see the interactive API documentation.

---

## Example API calls (using curl or Postman)

```bash
# Send a message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add task Finish the report"}'

# View all tasks
curl http://localhost:8000/tasks

# View all events
curl http://localhost:8000/events

# View all notes
curl http://localhost:8000/notes
```

---

## Project structure

```
productivity-assistant/
├── agents/
│   ├── primary_agent.py      ← Main coordinator (uses Gemini)
│   ├── task_agent.py         ← Manages tasks
│   ├── calendar_agent.py     ← Manages events
│   └── notes_agent.py        ← Manages notes
├── database/
│   └── db.py                 ← All database functions
├── api/
│   └── main.py               ← FastAPI server
├── requirements.txt
├── .env                      ← Your API key goes here
└── README.md
```

---

## Tech stack

| Tool | Purpose |
|------|---------|
| Python | Programming language |
| Google Gemini API | AI brain for understanding requests |
| SQLite | Database (built into Python, no extra setup) |
| FastAPI | Creates the HTTP API |
| uvicorn | Runs the FastAPI server |
