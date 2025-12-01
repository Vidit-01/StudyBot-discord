import json
import os
from src.config import DB_FILE
from src.utils import get_today_str

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}}
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"users": {}}

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_user_data(data, user_id):
    user_id = str(user_id)
    if user_id not in data["users"]:
        data["users"][user_id] = {
            "tasks": [],
            "history": {}
        }
    return data["users"][user_id]

def ensure_today_history(user_data):
    today = get_today_str()
    if today not in user_data["history"]:
        user_data["history"][today] = {}
    
    # Initialize missing tasks as False
    today_history = user_data["history"][today]
    for task in user_data["tasks"]:
        if task not in today_history:
            today_history[task] = False
    return today_history

def resolve_task(user_data, task_ref):
    tasks = user_data["tasks"]
    if not tasks:
        return None, "No tasks found."
    
    # Try index
    if task_ref.isdigit():
        idx = int(task_ref) - 1
        if 0 <= idx < len(tasks):
            return tasks[idx], None
        return None, "Invalid task number."
    
    # Try exact match
    if task_ref in tasks:
        return task_ref, None
        
    # Try partial match
    matches = [t for t in tasks if task_ref.lower() in t.lower()]
    if len(matches) == 1:
        return matches[0], None
    elif len(matches) > 1:
        return None, f"Multiple tasks match '{task_ref}': {', '.join(matches)}. Be more specific."
    
    return None, f"Task '{task_ref}' not found."
