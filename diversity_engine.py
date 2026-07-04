import difflib
import json
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
STATE_PATH = BASE_DIR / "memory" / "recent_responses.json"
MAX_RECENT = 30


def _normalize(text):
    text = str(text or "").strip().lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[ㅋㅎ.!?~…]", "", text)
    return text


def _ending(reply):
    lines = [line.strip() for line in str(reply or "").splitlines() if line.strip()]
    return lines[-1] if lines else ""


def _load():
    if not STATE_PATH.exists():
        return []
    try:
        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []
    return data if isinstance(data, list) else []


def _save(items):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(items[-MAX_RECENT:], ensure_ascii=False, indent=2), encoding="utf-8")


def remember_response(reply, category="default"):
    items = _load()
    items.append({"category": category, "reply": str(reply or ""), "ending": _ending(reply)})
    _save(items)


def similarity_to_recent(reply, category=None):
    normalized = _normalize(reply)
    if not normalized:
        return 0
    best = 0
    for item in _load()[-MAX_RECENT:]:
        old = item.get("reply", "")
        score = difflib.SequenceMatcher(None, normalized, _normalize(old)).ratio()
        if category and item.get("category") == category:
            score += 0.08
        best = max(best, min(score, 1))
    return best


def is_too_similar(reply, category=None, threshold=0.72):
    if similarity_to_recent(reply, category) >= threshold:
        return True
    ending = _ending(reply)
    if not ending:
        return False
    recent_endings = [_ending(item.get("reply", "")) for item in _load()[-5:]]
    return recent_endings.count(ending) >= 2


def retry_instruction(reply, category=None):
    return (
        "Diversity Engine: The draft is too similar to recent replies. "
        "Regenerate with a different opening, different structure, and different ending. "
        "Do not reuse this draft: " + str(reply or "")[:180]
    )
