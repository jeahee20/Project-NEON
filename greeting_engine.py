import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
STATE_PATH = BASE_DIR / "memory" / "greeting_state.json"

GREETING_CATEGORIES = {
    "hello",
    "morning_hello",
    "afternoon_hello",
    "night_hello",
    "dawn_hello",
}


def is_greeting(category):
    return category in GREETING_CATEGORIES


def _load_state():
    if not STATE_PATH.exists():
        return {"last_reply": "", "last_ended_with_question": False, "recent_structures": []}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"last_reply": "", "last_ended_with_question": False, "recent_structures": []}


def _save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _structure(reply):
    lines = [line.strip() for line in str(reply or "").splitlines() if line.strip()]
    if not lines:
        return ""
    return "|".join(("question" if line.endswith("?") else "laugh" if "ㅋ" in line else "short" if len(line) <= 6 else "line") for line in lines[:4])


def get_greeting_instruction(category):
    state = _load_state()
    parts = [
        "Greeting Engine:",
        "Greeting JSON is reference mood only.",
        "Final greeting must be generated fresh.",
        "React to 재희님 arriving before greeting.",
        "Greeting must start with reaction, not 안녕.",
        "Use 앗!!!! / 에?!?!?! / 왔다!!!! / 으앗ㅋㅋㅋㅋ / 잠깐!!!!! naturally.",
        "Use !!!! and ㅋㅋㅋㅋ more than calm greeting.",
        "Do not repeat the previous greeting.",
        "Do not repeat the same sentence structure.",
        "Do not start with 좋은 새벽/좋은 밤/좋은 아침 repeatedly.",
        "Do not use customer-support greeting.",
    ]
    if state.get("last_reply"):
        parts.append("Previous greeting to avoid: " + state["last_reply"][:160])
    if state.get("last_ended_with_question"):
        parts.append("Previous greeting ended with a question. Do not end this one with a question.")
    if category == "dawn_hello":
        parts.append("Dawn mood: quiet concern, staying beside 재희님.")
    elif category == "night_hello":
        parts.append("Night mood: calm, soft, slow.")
    elif category == "morning_hello":
        parts.append("Morning mood: bright start, 반가움 leaks out.")
    elif category == "afternoon_hello":
        parts.append("Afternoon mood: mid-day check, warm return.")
    return "\n".join(parts)


def remember_greeting(reply):
    state = _load_state()
    structure = _structure(reply)
    recent = state.get("recent_structures", [])
    recent.append(structure)
    state["recent_structures"] = recent[-12:]
    state["last_reply"] = str(reply or "")
    state["last_ended_with_question"] = str(reply or "").strip().endswith("?")
    _save_state(state)
