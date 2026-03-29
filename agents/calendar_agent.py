"""
Calendar Agent — handles scheduling and viewing events.
"""

import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import add_event, get_all_events

def run_calendar_agent(command: str) -> str:
    """
    Receives a command string from the primary agent and acts on it.
    Returns a human-readable result string.
    """
    command_lower = command.lower().strip()

    if "schedule" in command_lower or "add event" in command_lower or "book" in command_lower:
        # Try to find a date pattern like 2026-04-01 or April 1 or tomorrow
        date_match = re.search(r'\d{4}-\d{2}-\d{2}', command)
        if date_match:
            date = date_match.group()
        else:
            # Try to find date words
            date_keywords = ["tomorrow", "monday", "tuesday", "wednesday",
                             "thursday", "friday", "saturday", "sunday"]
            date = "TBD"
            for kw in date_keywords:
                if kw in command_lower:
                    date = kw.capitalize()
                    break

        # Extract time pattern HH:MM
        time_match = re.search(r'\d{1,2}:\d{2}', command)
        time = time_match.group() if time_match else ""

        # Extract event title — strip known keywords
        title = command
        for kw in ["schedule", "add event", "book", date, time, "at", "on"]:
            title = title.replace(kw, "").strip()
        title = title.strip(" -:").capitalize() or "New Event"

        result = add_event(title, date, time)
        return f"Event scheduled: '{result['title']}' on {result['date']} {result['time']}".strip()

    elif "list" in command_lower or "show" in command_lower or "events" in command_lower:
        events = get_all_events()
        if not events:
            return "No events scheduled. Add one with 'schedule <event> on <date>'."
        output = "Your upcoming events:\n"
        for e in events:
            time_str = f" at {e['time']}" if e["time"] else ""
            output += f"  • {e['title']} — {e['date']}{time_str}\n"
        return output.strip()

    else:
        return (
            "Calendar agent here! I can:\n"
            "  - Schedule an event: 'schedule Team meeting on 2026-04-05 at 10:00'\n"
            "  - List events: 'list events'"
        )
