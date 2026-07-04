import json
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
HISTORY_PATH = BASE_DIR / "memory" / "conversation_history.json"
MAX_HISTORY = 40


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _load():
    if not HISTORY_PATH.exists():
        return []
    try:
        data = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []
    return data if isinstance(data, list) else []


def _save(history):
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_PATH.write_text(json.dumps(history[-MAX_HISTORY:], ensure_ascii=False, indent=2), encoding="utf-8")


def add_user_message(message, category=None, intent=None):
    history = _load()
    history.append(
        {
            "time": _now(),
            "speaker": "user",
            "message": str(message or ""),
            "category": category,
            "intent": intent,
        }
    )
    _save(history)


def add_neon_message(message, category=None, intent=None):
    history = _load()
    history.append(
        {
            "time": _now(),
            "speaker": "neon",
            "message": str(message or ""),
            "category": category,
            "intent": intent,
        }
    )
    _save(history)


def get_recent(limit=10):
    return _load()[-limit:]


def get_recent_text(limit=10):
    lines = []
    for item in get_recent(limit):
        speaker = "재희님" if item.get("speaker") == "user" else "NEON"
        message = str(item.get("message", "")).strip()
        if message:
            lines.append(f"{speaker}: {message}")
    return "\n".join(lines)


def get_last_user_message():
    for item in reversed(_load()):
        if item.get("speaker") == "user":
            return item
    return None


def get_last_topic():
    for item in reversed(_load()):
        category = item.get("category")
        intent = item.get("intent")
        if category in ("project", "music", "game", "comfort") or intent in ("Project", "Music", "Game", "Comfort"):
            return intent or category
    return None
