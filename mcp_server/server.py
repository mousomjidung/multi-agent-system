"""
Standalone MCP server. Can run via stdio OR streamable-http.
When used with ADK StdioConnectionParams, ADK spawns this as a subprocess.
"""
import json
import sys
import os

# Ensure parent dir is in path so database imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP

server = FastMCP("multi-agent-tools")

# ═══ TASK TOOLS ═══
@server.tool()
def create_task(title: str, description: str = "", priority: str = "medium") -> str:
    """Create a new task with title, optional description, and priority (low/medium/high)."""
    from database.firestore_client import create_task as db_fn
    return json.dumps({"status": "success", "message": f"Task '{title}' created.", "task": db_fn(title=title, description=description, priority=priority)})

@server.tool()
def list_tasks(status: str = "") -> str:
    """List all tasks, optionally filtered by status (pending/in_progress/completed)."""
    from database.firestore_client import list_tasks as db_fn
    r = db_fn(status=status)
    return json.dumps({"status": "success", "count": len(r), "tasks": r})

@server.tool()
def update_task(task_id: str, status: str = "", title: str = "", description: str = "", priority: str = "") -> str:
    """Update a task's status, title, description, or priority."""
    from database.firestore_client import update_task as db_fn
    kw = {k: v for k, v in {"status": status, "title": title, "description": description, "priority": priority}.items() if v}
    if not kw: return json.dumps({"status": "error", "message": "No updates provided."})
    r = db_fn(task_id, **kw)
    return json.dumps({"status": "success", "task": r} if r else {"status": "error", "message": f"Task '{task_id}' not found."})

@server.tool()
def get_task(task_id: str) -> str:
    """Get details of a specific task by ID."""
    from database.firestore_client import get_task as db_fn
    r = db_fn(task_id)
    return json.dumps({"status": "success", "task": r} if r else {"status": "error", "message": f"Task '{task_id}' not found."})

# ═══ CALENDAR TOOLS ═══
@server.tool()
def schedule_event(title: str, date: str, time: str = "09:00", description: str = "") -> str:
    """Schedule a new calendar event. date=YYYY-MM-DD, time=HH:MM."""
    from database.firestore_client import create_event as db_fn
    return json.dumps({"status": "success", "message": f"Event '{title}' scheduled for {date} at {time}.", "event": db_fn(title=title, date=date, time=time, description=description)})

@server.tool()
def list_events(date: str = "") -> str:
    """List calendar events, optionally filtered by date (YYYY-MM-DD)."""
    from database.firestore_client import list_events as db_fn
    r = db_fn(date=date)
    return json.dumps({"status": "success", "count": len(r), "events": r})

@server.tool()
def update_event(event_id: str, title: str = "", date: str = "", time: str = "", description: str = "") -> str:
    """Update a calendar event."""
    from database.firestore_client import update_event as db_fn
    kw = {k: v for k, v in {"title": title, "date": date, "time": time, "description": description}.items() if v}
    if not kw: return json.dumps({"status": "error", "message": "No updates provided."})
    r = db_fn(event_id, **kw)
    return json.dumps({"status": "success", "event": r} if r else {"status": "error", "message": f"Event '{event_id}' not found."})

# ═══ NOTES TOOLS ═══
@server.tool()
def save_note(title: str, content: str, tags: str = "") -> str:
    """Save a new note with title, content, and optional comma-separated tags."""
    from database.firestore_client import create_note as db_fn
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    return json.dumps({"status": "success", "message": f"Note '{title}' saved.", "note": db_fn(title=title, content=content, tags=tag_list)})

@server.tool()
def list_notes(tag: str = "") -> str:
    """List notes, optionally filtered by tag."""
    from database.firestore_client import list_notes as db_fn
    r = db_fn(tag=tag)
    return json.dumps({"status": "success", "count": len(r), "notes": r})

@server.tool()
def update_note(note_id: str, title: str = "", content: str = "", tags: str = "") -> str:
    """Update an existing note."""
    from database.firestore_client import update_note as db_fn
    kw = {}
    if title: kw["title"] = title
    if content: kw["content"] = content
    if tags: kw["tags"] = [t.strip() for t in tags.split(",") if t.strip()]
    if not kw: return json.dumps({"status": "error", "message": "No updates provided."})
    r = db_fn(note_id, **kw)
    return json.dumps({"status": "success", "note": r} if r else {"status": "error", "message": f"Note '{note_id}' not found."})

if __name__ == "__main__":
    server.run(transport="stdio")
