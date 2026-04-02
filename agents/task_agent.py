import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import add_task, get_all_tasks, complete_task

def run_task_agent(command: str) -> str:
    command_lower = command.lower().strip()

    priority = "medium"
    if "high" in command_lower or "urgent" in command_lower or "important" in command_lower:
        priority = "high"
    elif "low" in command_lower or "later" in command_lower:
        priority = "low"

    priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}

    if "add" in command_lower or "create" in command_lower or "new task" in command_lower:
        for keyword in ["add task", "create task", "new task", "add"]:
            if keyword in command_lower:
                title = command_lower.replace(keyword, "").strip()
                for p in ["high priority", "low priority", "medium priority", "high", "low", "urgent", "important", "later"]:
                    title = title.replace(p, "").strip()
                title = title.capitalize()
                if title:
                    result = add_task(title, priority=priority)
                    return f"Task added: {priority_icon[priority]} '{result['title']}' [{priority.upper()} priority] (ID: {result['id']})"
        return "Please specify a task title. Example: 'Add task Buy groceries high priority'"

    elif "list" in command_lower or "show" in command_lower or "all tasks" in command_lower:
        tasks = get_all_tasks()
        if not tasks:
            return "No tasks found. Add one with 'Add task <title>'"
        output = "Your tasks:\n"
        for t in tasks:
            status_icon = "✓" if t["status"] == "done" else "○"
            p = t.get("priority", "medium")
            icon = priority_icon.get(p, "🟡")
            output += f"  [{status_icon}] ID {t['id']}: {icon} {t['title']} [{p.upper()}]\n"
        return output.strip()

    elif "complete" in command_lower or "done" in command_lower or "finish" in command_lower:
        numbers = re.findall(r'\d+', command)
        if numbers:
            complete_task(int(numbers[0]))
            return f"Task {numbers[0]} marked as completed! ✓"
        return "Please provide the task ID. Example: 'Complete task 3'"

    else:
        return (
            "Task agent here! I can:\n"
            "  - Add task: 'Add task Buy groceries high priority'\n"
            "  - List tasks: 'List tasks'\n"
            "  - Complete task: 'Complete task 3'"
        )
