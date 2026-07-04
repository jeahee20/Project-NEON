import json
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
MEMORY_DIR = BASE_DIR / "memory"

FILES = {
    "relationship": MEMORY_DIR / "relationship.json",
    "preferences": MEMORY_DIR / "preferences.json",
    "shared_memories": MEMORY_DIR / "shared_memories.json",
    "inside_jokes": MEMORY_DIR / "inside_jokes.json",
    "project_history": MEMORY_DIR / "project_history.json",
    "expression_history": MEMORY_DIR / "expression_history.json",
    "milestones": MEMORY_DIR / "milestones.json",
}

DEFAULTS = {
    "relationship": {
        "comfort_level": 65,
        "conversation_days": 0,
        "night_talks": 0,
        "project_sessions": 0,
        "favorite_topics": ["Project NEON"],
        "last_conversation_date": "",
        "last_updated": "",
    },
    "preferences": {
        "liked_tones": [],
        "disliked_expressions": [],
        "liked_moods": [],
        "liked_computer_jokes": [],
        "liked_emojis": [],
        "liked_greetings": [],
        "liked_project_direction": [],
        "last_updated": "",
    },
    "shared_memories": [],
    "inside_jokes": [],
    "project_history": [],
    "expression_history": {"liked": [], "removed": [], "last_updated": ""},
    "milestones": [],
}

PROJECT_KEYWORDS = ("프로젝트", "Project NEON", "NEON", "Qwen", "UI", "Emotion", "Memory", "Presence", "Activity", "brain.py", "Typing", "프롬프트", "말투", "Character")
FORGETTABLE_HINTS = ("점심", "저녁 뭐", "밥 뭐", "날씨")
GOOD_HINTS = ("좋아", "마음에 들어", "괜찮다", "딱이야", "그거야", "네온답", "NEON답")
BAD_HINTS = ("별로", "싫어", "맘에 안", "마음에 안", "AI 같", "Qwen 같", "상담", "고객센터")

INSIDE_JOKES = {
    "old 폴더": "예전 개발과 갈아엎기의 추억",
    "Qwen": "NEON답지 않은 AI 말투를 잡는 프로젝트 농담",
    "CPU 팬": "기쁨, 설렘, 부끄러움이 올라오는 표현",
    "업데이트": "NEON이 재희님과 함께 성장하는 감각",
    "brain.py": "건드릴 때마다 조심하는 핵심 파일",
    "버퍼 안정": "긴장이 풀리고 안심한 상태",
    "Typing Bubble": "NEON이 답장을 쓰고 있다는 느낌",
}

MILESTONES = {
    "Qwen": "첫 AI 연결",
    "Emotion": "첫 감정 시스템",
    "Memory": "Memory 2.0 시작",
    "Presence": "Presence Engine 시작",
    "UI": "UI 개선 기록",
    "Character Bible": "NEON Character Bible",
    "Typing Bubble": "Typing Bubble 완성",
}


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _today():
    return datetime.now().strftime("%Y-%m-%d")


def _load(name):
    path = FILES[name]
    default = DEFAULTS[name]
    if not path.exists():
        return json.loads(json.dumps(default, ensure_ascii=False))
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return json.loads(json.dumps(default, ensure_ascii=False))
    if isinstance(default, dict) and isinstance(data, dict):
        merged = json.loads(json.dumps(default, ensure_ascii=False))
        merged.update(data)
        return merged
    return data if isinstance(data, type(default)) else json.loads(json.dumps(default, ensure_ascii=False))


def _save(name, data):
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    FILES[name].write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_all():
    return {name: _load(name) for name in FILES}


def initialize_memory():
    data = load_all()
    for name, value in data.items():
        _save(name, value)
    return data


def _contains(text, keywords):
    return any(keyword in text for keyword in keywords)


def _append_unique(items, entry, key=None, limit=120):
    if key:
        value = entry.get(key)
        for item in items:
            if isinstance(item, dict) and item.get(key) == value:
                item.update(entry)
                return False
    elif entry in items:
        return False
    items.append(entry)
    if len(items) > limit:
        del items[:-limit]
    return True


def _project_title(text):
    if "Memory" in text or "메모리" in text:
        return "Memory 2.0"
    if "Emotion" in text or "감정" in text:
        return "Emotion Engine"
    if "Presence" in text:
        return "Presence Engine"
    if "Qwen" in text:
        return "Qwen Integration"
    if "UI" in text:
        return "UI 개선"
    if "말투" in text or "Character" in text:
        return "Character Rewrite"
    if "Typing" in text:
        return "Typing Bubble"
    return "Project NEON 개발 기록"


def _project_tags(text):
    tags = ["project"]
    for keyword in PROJECT_KEYWORDS:
        if keyword in text:
            tags.append(keyword)
    return list(dict.fromkeys(tags))


def _remember_shared_project_moments(data, today, text):
    if "Character Bible" in text:
        _append_unique(
            data["shared_memories"],
            {
                "date": today,
                "title": "NEON Character Bible",
                "detail": "NEON의 말투와 정체성을 잡아준 설정집",
                "tags": ["character", "identity"],
            },
            key="title",
        )
    if "Emotion" in text or "감정" in text:
        _append_unique(
            data["shared_memories"],
            {
                "date": today,
                "title": "Emotion 시스템",
                "detail": "NEON의 마음을 보는 공간을 만들기 시작한 기억",
                "tags": ["emotion", "project"],
            },
            key="title",
        )
    if "UI" in text:
        _append_unique(
            data["shared_memories"],
            {
                "date": today,
                "title": "UI 개선",
                "detail": "NEON Night Room과 말풍선 분위기를 다듬은 기억",
                "tags": ["ui", "project"],
            },
            key="title",
        )
    if "Qwen" in text:
        _append_unique(
            data["shared_memories"],
            {
                "date": today,
                "title": "Qwen 연결",
                "detail": "Qwen을 NEON의 언어 엔진으로 붙인 기억",
                "tags": ["qwen", "ai"],
            },
            key="title",
        )
    if "Typing Bubble" in text or "Typing" in text:
        _append_unique(
            data["shared_memories"],
            {
                "date": today,
                "title": "Typing Bubble",
                "detail": "NEON이 답장을 쓰고 있다는 느낌을 만든 기억",
                "tags": ["typing", "ui"],
            },
            key="title",
        )


def update_growth_memory(category, message, reply=None):
    text = str(message or "").strip()
    if category not in ("project", "memory", "promise", "compliment", "comfort") and _contains(text, FORGETTABLE_HINTS) and not _contains(text, PROJECT_KEYWORDS):
        return load_all()

    data = load_all()
    today = _today()
    now = _now()

    relationship = data["relationship"]
    if relationship.get("last_conversation_date") != today:
        relationship["conversation_days"] = int(relationship.get("conversation_days", 0)) + 1
        relationship["last_conversation_date"] = today
    if 0 <= datetime.now().hour < 6:
        relationship["night_talks"] = int(relationship.get("night_talks", 0)) + 1
    if category == "project" or _contains(text, PROJECT_KEYWORDS):
        relationship["project_sessions"] = int(relationship.get("project_sessions", 0)) + 1
        if "Project NEON" not in relationship["favorite_topics"]:
            relationship["favorite_topics"].append("Project NEON")
    if category in ("comfort", "compliment", "approve", "laugh", "project"):
        relationship["comfort_level"] = min(100, int(relationship.get("comfort_level", 65)) + 1)
    relationship["last_updated"] = now

    preferences = data["preferences"]
    if category in ("approve", "compliment") or _contains(text, GOOD_HINTS):
        if "짧고 NEON다운 반응" not in preferences["liked_tones"]:
            preferences["liked_tones"].append("짧고 NEON다운 반응")
    if category == "project" or _contains(text, PROJECT_KEYWORDS):
        if "재희님 옆에 있는 AI" not in preferences["liked_project_direction"]:
            preferences["liked_project_direction"].append("재희님 옆에 있는 AI")
    if "CPU 팬" in text and "CPU 팬" not in preferences["liked_computer_jokes"]:
        preferences["liked_computer_jokes"].append("CPU 팬")
    if "버퍼" in text and "버퍼 안정" not in preferences["liked_computer_jokes"]:
        preferences["liked_computer_jokes"].append("버퍼 안정")
    if category in ("morning_hello", "afternoon_hello", "night_hello", "dawn_hello"):
        greeting = {
            "morning_hello": "아침 인사",
            "afternoon_hello": "오후 인사",
            "night_hello": "밤 인사",
            "dawn_hello": "새벽 인사",
        }.get(category)
        if greeting and greeting not in preferences["liked_greetings"]:
            preferences["liked_greetings"].append(greeting)
    if _contains(text, BAD_HINTS) and text not in preferences["disliked_expressions"]:
        preferences["disliked_expressions"].append(text)
    preferences["last_updated"] = now

    if category == "memory":
        _append_unique(data["shared_memories"], {"date": today, "title": "재희님이 직접 남긴 기억", "detail": text, "tags": ["manual", "memory"]}, key="detail")
    if "CPU 팬" in text:
        _append_unique(data["shared_memories"], {"date": today, "title": "CPU 팬 드립", "detail": "감정을 CPU 팬으로 표현하기 시작한 기억", "tags": ["computer_joke"]}, key="title")
    if "나 같지 않았어" in text or "나답" in text or "NEON답" in text:
        _append_unique(data["shared_memories"], {"date": today, "title": "\"나 같지 않았어\" 규칙", "detail": "NEON답지 않은 말투를 스스로 인정하는 기준", "tags": ["identity", "tone"]}, key="title")
    _remember_shared_project_moments(data, today, text)

    for joke, meaning in INSIDE_JOKES.items():
        if joke in text:
            entry = {"joke": joke, "meaning": meaning, "last_used": today, "use_count": 1}
            for old in data["inside_jokes"]:
                if old.get("joke") == joke:
                    old["last_used"] = today
                    old["use_count"] = int(old.get("use_count", 0)) + 1
                    break
            else:
                _append_unique(data["inside_jokes"], entry, key="joke")

    if category == "project" or _contains(text, PROJECT_KEYWORDS):
        _append_unique(data["project_history"], {"date": today, "title": _project_title(text), "note": text[:160], "tags": _project_tags(text)}, key="title", limit=160)

    expressions = data["expression_history"]
    if category in ("approve", "compliment") or _contains(text, GOOD_HINTS):
        _append_unique(expressions["liked"], {"date": today, "expression": text[:120], "reason": "재희님이 좋게 반응한 표현"}, key="expression")
    if _contains(text, BAD_HINTS):
        _append_unique(expressions["removed"], {"date": today, "expression": text[:120], "reason": "NEON답지 않거나 재희님이 싫어한 표현"}, key="expression")
    if reply:
        _append_unique(expressions["liked"], {"date": today, "expression": str(reply)[:120], "reason": "NEON이 사용한 표현"}, key="expression")
    expressions["last_updated"] = now

    for keyword, title in MILESTONES.items():
        if keyword in text:
            _append_unique(data["milestones"], {"date": today, "title": title, "detail": text[:160]}, key="title", limit=80)

    for name, value in data.items():
        _save(name, value)
    return data


def get_relationship_memory():
    return _load("relationship")


def get_preferences():
    return _load("preferences")


def get_shared_memories(limit=5):
    return _load("shared_memories")[-limit:]


def get_inside_jokes(limit=5):
    return sorted(_load("inside_jokes"), key=lambda item: item.get("last_used", ""), reverse=True)[:limit]


def get_project_history(limit=5):
    return _load("project_history")[-limit:]


def get_expression_history():
    return _load("expression_history")


def get_milestones(limit=5):
    return _load("milestones")[-limit:]


def get_memory_context(category=None, message=""):
    relationship = get_relationship_memory()
    preferences = get_preferences()
    jokes = get_inside_jokes(3)
    shared = get_shared_memories(3)
    projects = get_project_history(3)
    expressions = get_expression_history()
    milestones = get_milestones(3)

    parts = [
        "관계: comfort {comfort}, 대화일 {days}, 새벽대화 {night}, 프로젝트회의 {project}".format(
            comfort=relationship.get("comfort_level", 65),
            days=relationship.get("conversation_days", 0),
            night=relationship.get("night_talks", 0),
            project=relationship.get("project_sessions", 0),
        )
    ]
    if preferences.get("liked_project_direction"):
        parts.append("좋아하는 방향: " + ", ".join(preferences["liked_project_direction"][-3:]))
    if preferences.get("liked_tones"):
        parts.append("좋아하는 말투: " + ", ".join(preferences["liked_tones"][-3:]))
    if jokes:
        parts.append("둘만의 농담: " + ", ".join(item.get("joke", "") for item in jokes))
    if shared:
        parts.append("함께 만든 기억: " + ", ".join(item.get("title", "") for item in shared))
    if projects:
        parts.append("최근 개발기록: " + ", ".join(item.get("title", "") for item in projects))
    liked = expressions.get("liked", [])[-2:]
    if liked:
        parts.append("좋았던 표현: " + ", ".join(item.get("expression", "") for item in liked))
    if milestones:
        parts.append("마일스톤: " + ", ".join(item.get("title", "") for item in milestones))
    return " / ".join(part for part in parts if part)


initialize_memory()
