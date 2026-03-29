"""
Notes Agent — saves and retrieves notes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import add_note, get_all_notes

def run_notes_agent(command: str) -> str:
    """
    Receives a command string from the primary agent and acts on it.
    Returns a human-readable result string.
    """
    command_lower = command.lower().strip()

    if "save note" in command_lower or "add note" in command_lower or "note:" in command_lower:
        # Format expected: "save note: Title | Content"
        # or: "save note Buy milk and eggs"
        content_part = command
        for kw in ["save note", "add note", "note:"]:
            content_part = content_part.replace(kw, "").replace(kw.lower(), "").strip()

        if "|" in content_part:
            parts = content_part.split("|", 1)
            title = parts[0].strip().capitalize()
            content = parts[1].strip()
        else:
            # Use first few words as the title
            words = content_part.split()
            title = " ".join(words[:4]).capitalize() if words else "Note"
            content = content_part

        if not content:
            return "Please provide content for the note. Example: 'save note: Shopping list | Buy milk and eggs'"

        result = add_note(title, content)
        return f"Note saved: '{result['title']}'"

    elif "list" in command_lower or "show notes" in command_lower or "my notes" in command_lower:
        notes = get_all_notes()
        if not notes:
            return "No notes yet. Save one with 'save note: Title | Content'"
        output = "Your notes:\n"
        for n in notes:
            preview = n["content"][:60] + "..." if len(n["content"]) > 60 else n["content"]
            output += f"  • {n['title']}: {preview}\n"
        return output.strip()

    else:
        return (
            "Notes agent here! I can:\n"
            "  - Save a note: 'save note: Meeting notes | We discussed the Q2 plan'\n"
            "  - List notes: 'list notes'"
        )
