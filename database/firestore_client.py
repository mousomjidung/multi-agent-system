"""
Firestore operations for tasks, events, and notes.
Collections: tasks | events | notes
"""
from google.cloud import firestore
from datetime import datetime, timezone
import uuid

db = firestore.Client()

def _now():
    return datetime.now(timezone.utc).isoformat()

def _id():
    return uuid.uuid4().hex[:8]

# ── TASKS ──

def create_task(title, description="", priority="medium"):
    tid = _id()
    data = {"id": tid, "title": title, "description": description,
            "status": "pending", "priority": priority,
            "created_at": _now(), "updated_at": _now()}
    db.collection("tasks").document(tid).set(data)
    return data

def list_tasks(status=""):
    q = db.collection("tasks")
    if status:
        q = q.where("status", "==", status)
    return [d.to_dict() for d in q.stream()]

def get_task(task_id):
    doc = db.collection("tasks").document(task_id).get()
    return doc.to_dict() if doc.exists else None

def update_task(task_id, **kwargs):
    ref = db.collection("tasks").document(task_id)
    if not ref.get().exists:
        return None
    kwargs["updated_at"] = _now()
    ref.update(kwargs)
    return ref.get().to_dict()

# ── EVENTS ──

def create_event(title, date, time="09:00", description=""):
    eid = _id()
    data = {"id": eid, "title": title, "date": date, "time": time,
            "description": description, "created_at": _now()}
    db.collection("events").document(eid).set(data)
    return data

def list_events(date=""):
    q = db.collection("events")
    if date:
        q = q.where("date", "==", date)
    return [d.to_dict() for d in q.stream()]

def update_event(event_id, **kwargs):
    ref = db.collection("events").document(event_id)
    if not ref.get().exists:
        return None
    ref.update(kwargs)
    return ref.get().to_dict()

# ── NOTES ──

def create_note(title, content, tags=None):
    nid = _id()
    data = {"id": nid, "title": title, "content": content,
            "tags": tags or [], "created_at": _now(), "updated_at": _now()}
    db.collection("notes").document(nid).set(data)
    return data

def list_notes(tag=""):
    q = db.collection("notes")
    if tag:
        q = q.where("tags", "array_contains", tag)
    return [d.to_dict() for d in q.stream()]

def update_note(note_id, **kwargs):
    ref = db.collection("notes").document(note_id)
    if not ref.get().exists:
        return None
    kwargs["updated_at"] = _now()
    ref.update(kwargs)
    return ref.get().to_dict()
