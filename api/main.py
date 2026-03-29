"""
FastAPI server — exposes the multi-agent assistant as an HTTP API.
Run with: uvicorn api.main:app --reload
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from pydantic import BaseModel
from database.db import setup_database
from agents.primary_agent import run_primary_agent

# Create the FastAPI app
app = FastAPI(
    title="Multi-Agent Productivity Assistant",
    description="An AI assistant that manages your tasks, calendar, and notes.",
    version="1.0.0"
)

# Set up the database when the server starts
@app.on_event("startup")
def startup_event():
    setup_database()
    print("Server started. Database ready.")

# Define the request body structure
class UserRequest(BaseModel):
    message: str

# Define the response structure
class AssistantResponse(BaseModel):
    message: str
    response: str

# Main endpoint — send a message, get a response
@app.post("/chat", response_model=AssistantResponse)
def chat(request: UserRequest):
    """
    Send a message to the assistant.
    Example body: {"message": "Add task Finish the report"}
    """
    result = run_primary_agent(request.message)
    return AssistantResponse(message=request.message, response=result)

# Health check endpoint
@app.get("/")
def root():
    return {"status": "running", "message": "Productivity Assistant API is live!"}

# View all data endpoints (useful for demo)
@app.get("/tasks")
def list_tasks():
    from database.db import get_all_tasks
    return {"tasks": get_all_tasks()}

@app.get("/events")
def list_events():
    from database.db import get_all_events
    return {"events": get_all_events()}

@app.get("/notes")
def list_notes():
    from database.db import get_all_notes
    return {"notes": get_all_notes()}

from fastapi.responses import FileResponse

@app.get("/app")
def serve_chat():
    return FileResponse("chat.html")
