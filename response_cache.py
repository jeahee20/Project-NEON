import json
import random
from pathlib import Path

import dialogue_loader


BASE_DIR = Path(__file__).resolve().parent
CACHE_PATH = BASE_DIR / "assets" / "dialogues" / "response_cache.json"

CACHEABLE_CATEGORIES = {
    "approve",
    "ack",
    "soft_ack",
    "laugh",
    "thanks",
    "compliment",
    "daily",
    "memory",
    "promise",
}

CACHEABLE_TEXTS = {
    "좋아",
    "웅",
    "응",
    "그래",
    "오케이",
    "ㅇㅋ",
    "굿",
    "맞아",
    "ㅋㅋ",
    "ㅎㅎ",
    "잘자",
    "고마워",
}

_cache = None
_last_reply = {}


def _key(message, category):
    return f"{category}:{str(message or '').strip()}"


def _load_cache():
    global _cache

    if _cache is not None:
        return _cache

    if not CACHE_PATH.exists():
        _cache = {}
        return _cache

    try:
        _cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        _cache = {}

    return _cache


def _save_cache():
    if _cache is None:
        return

    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(_cache, ensure_ascii=False, indent=2), encoding="utf-8")


def is_cacheable(message, category):
    text = str(message or "").strip()
    compact = text.replace(" ", "")

    if category in CACHEABLE_CATEGORIES:
        return True

    if compact in CACHEABLE_TEXTS:
        return True

    if len(compact) <= 8 and category not in ("project", "comfort", "question"):
        return True

    return False


def _pick_no_repeat(key, replies):
    if not replies:
        return None

    candidates = [reply for reply in replies if reply and reply != _last_reply.get(key)]
    if not candidates:
        candidates = [reply for reply in replies if reply]

    if not candidates:
        return None

    reply = random.choice(candidates)
    _last_reply[key] = reply
    return reply


def _dialogue_replies(category):
    dialogues = dialogue_loader.load_dialogues(category)
    replies = []

    for item in dialogues:
        neon = item.get("neon") if isinstance(item, dict) else None
        if neon:
            replies.append(neon)

    return replies


def get_cached_reply(message, category):
    if not is_cacheable(message, category):
        return None

    key = _key(message, category)
    cache = _load_cache()
    replies = list(cache.get(key, []))

    if replies:
        print("[CACHE] HIT")
        return _pick_no_repeat(key, replies)

    replies = _dialogue_replies(category)
    if replies:
        print("[CACHE] DIALOGUE")
        return _pick_no_repeat(key, replies)

    return None


def store_reply(message, category, reply):
    if not reply or not is_cacheable(message, category):
        return

    key = _key(message, category)
    cache = _load_cache()
    replies = cache.setdefault(key, [])

    if reply not in replies:
        replies.append(reply)
        if len(replies) > 24:
            del replies[:-24]
        _save_cache()
