import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google import genai
from dotenv import load_dotenv
from agents.task_agent import run_task_agent
from agents.calendar_agent import run_calendar_agent
from agents.notes_agent import run_notes_agent

load_dotenv(dotenv_path="env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are a coordinator AI. Read the user message and reply with ONLY one word:
- TASK      if the user wants to add, list, or complete tasks
- CALENDAR  if the user wants to schedule or view events
- NOTES     if the user wants to save or view notes
- UNKNOWN   if none of the above"""

def classify_intent(user_message):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\nUser message: {user_message}"
    )
    intent = response.text.strip().upper()
    if intent not in ["TASK", "CALENDAR", "NOTES"]:
        return "UNKNOWN"
    return intent

def run_primary_agent(user_message):
    print(f"\nUser: {user_message}")
    intent = classify_intent(user_message)
    print(f"Intent: {intent}")
    if intent == "TASK":
        result = run_task_agent(user_message)
    elif intent == "CALENDAR":
        result = run_calendar_agent(user_message)
    elif intent == "NOTES":
        result = run_notes_agent(user_message)
    else:
        result = "I'm not sure. Try: 'Add task X', 'Schedule event on date', 'Save note: Title | Content'"
    print(f"Assistant: {result}")
    return result

if __name__ == "__main__":
    from database.db import setup_database
    setup_database()
    print("=== Multi-Agent Productivity Assistant ===")
    print("Type your request. Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["quit", "exit"]:
            break
        if not user_input:
            continue
        run_primary_agent(user_input)
