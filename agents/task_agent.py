"""
Task Agent — handles everything related to tasks.
It receives a plain-English command and performs the right database action.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import add_task, get_all_tasks, complete_task

def run_task_agent(command: str) -> str:
    """
    Receives a command string from the primary agent and acts on it.
    Returns a human-readable result string.
    """
    command = command.lower().strip()

    if "add" in command or "create" in command or "new task" in command:
        # Extract task title from the command
        # Example: "add task Buy groceries"
        for keyword in ["add task", "create task", "new task", "add"]:
            if keyword in command:
                title = command.replace(keyword, "").strip().capitalize()
                if title:
                    result = add_task(title)
                    return f"Task added: '{result['title']}' (ID: {result['id']})"
        return "Please specify a task title. Example: 'add task Buy groceries'"

    elif "list" in command or "show" in command or "all tasks" in command:
        tasks = get_all_tasks()
        if not tasks:
            return "No tasks found. Add one with 'add task <name>'."
        output = "Your tasks:\n"
        for t in tasks:
            status_icon = "✓" if t["status"] == "done" else "○"
            output += f"  [{status_icon}] ID {t['id']}: {t['title']}\n"
        return output.strip()

    elif "complete" in command or "done" in command or "finish" in command:
        # Extract task ID — look for a number in the command
        import re
        numbers = re.findall(r'\d+', command)
        if numbers:
            task_id = int(numbers[0])
            complete_task(task_id)
            return f"Task {task_id} marked as completed!"
        return "Please provide the task ID. Example: 'complete task 3'"

    else:
        return (
            "Task agent here! I can:\n"
            "  - Add a task: 'add task <title>'\n"
            "  - List tasks: 'list tasks'\n"
            "  - Complete a task: 'complete task <id>'"
        )
