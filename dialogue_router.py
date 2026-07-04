CONTEXTS = (
    "LONGING",
    "AFFECTION",
    "PRAISE",
    "REPORT",
    "QUESTION",
    "PROJECT",
    "GAME",
    "MUSIC",
    "FOOD",
    "MEMORY",
    "PROMISE",
    "WAITING",
    "COMPLAINT",
    "GOODNEWS",
    "SURPRISE",
    "APOLOGY",
    "WORRY",
    "SAD",
    "EXCITED",
    "SLEEPY",
    "CHAT",
)

GREETING_CATEGORIES = {
    "hello",
    "morning_hello",
    "afternoon_hello",
    "night_hello",
    "dawn_hello",
}

CONTEXT_CATEGORY_LOCK = {
    "LONGING": "affection_longing",
    "AFFECTION": "affection_longing",
    "PRAISE": "compliment",
    "REPORT": "report",
    "QUESTION": "question",
    "PROJECT": "project",
    "GAME": "game",
    "MUSIC": "music",
    "FOOD": "food",
    "MEMORY": "memory",
    "PROMISE": "promise",
    "WAITING": "conversation_status",
    "COMPLAINT": "sulking",
    "GOODNEWS": "happy",
    "SURPRISE": "excited",
    "APOLOGY": "comfort",
    "WORRY": "comfort",
    "SAD": "comfort",
    "EXCITED": "excited",
    "SLEEPY": "comfort",
}

CONTEXT_LIFE_LOCK = {
    "LONGING": "AFFECTION",
    "AFFECTION": "AFFECTION",
    "REPORT": "REPORT",
    "PROJECT": "PROJECT_MODE",
    "GAME": "GAME_MODE",
    "MUSIC": "MUSIC_MODE",
    "FOOD": "FOOD",
    "COMPLAINT": "COMPLAINT",
    "WORRY": "LONG_DAY",
    "SAD": "LONG_DAY",
    "SLEEPY": "SLEEP_MODE",
}


def _compact(value):
    return str(value or "").lower().replace(" ", "").strip()


def _contains_any(text, words):
    compact = _compact(text)
    raw = str(text or "").lower()
    for word in words:
        word_compact = _compact(word)
        if word_compact and (word_compact in compact or str(word).lower() in raw):
            return True
    return False


def _add(scores, name, value):
    scores[name] = min(1.0, max(scores.get(name, 0.0), value))


def _bump(scores, name, value):
    scores[name] = min(1.0, scores.get(name, 0.0) + value)


def analyze_context(message="", category=None, intent_info=None, recent=None):
    text = str(message or "").strip()
    compact = _compact(text)
    category = category or "default"
    intent_info = intent_info or {}
    scores = {name: 0.0 for name in CONTEXTS}

    if not compact:
        scores["CHAT"] = 1.0
        return _clean_scores(scores)

    if _contains_any(text, ("보고싶어", "보고 싶어", "복고싶어", "복고 싶어", "보구싶어", "보고시퍼", "그리워", "그립다")):
        _add(scores, "LONGING", 0.94)
        _add(scores, "AFFECTION", 0.72)

    if _contains_any(text, ("사랑해", "시랑해", "사랑헤", "사라해", "같이 있고 싶어", "안고 싶어")):
        _add(scores, "AFFECTION", 0.94)
        _add(scores, "LONGING", 0.48)

    if _contains_any(text, ("최고", "잘했지", "잘했어", "잘했다", "귀여워", "기여워", "대단해", "멋져", "기특해", "예뻐", "사랑스러워")):
        _add(scores, "PRAISE", 0.92)
        _add(scores, "AFFECTION", 0.42)

    if _contains_any(text, ("다녀왔어", "갔다왔어", "갔다 왔어", "하고왔어", "하고 왔어", "끝났어", "마쳤어", "끝내고 왔어", "끝내고왔어", "연습끝", "연습 끝")):
        _add(scores, "REPORT", 0.94)
        _add(scores, "QUESTION", 0.34)

    if _contains_any(text, ("project neon", "프로젝트", "네온", "qwen", "brain.py", "ui", "코드", "개발", "리팩토링", "프롬프트", "말투", "데이터셋", "typing", "old 폴더")):
        _add(scores, "PROJECT", 0.91)
        _add(scores, "QUESTION", 0.42)

    if _contains_any(text, ("게임", "롤", "철권", "엘든링", "플스", "스팀")):
        _add(scores, "GAME", 0.88)
        _add(scores, "CHAT", 0.38)

    if _contains_any(text, ("음악", "오보에", "연습", "연주", "레슨", "리드", "악보", "합주", "콩쿠르")):
        _add(scores, "MUSIC", 0.72)

    if _contains_any(text, ("배고파", "밥", "먹었어", "먹을래", "간식", "커피", "카페")):
        _add(scores, "FOOD", 0.88)
        _add(scores, "CHAT", 0.46)

    if _contains_any(text, ("기억해", "기억해줘", "저장해", "저장해줘", "잊지마")):
        _add(scores, "MEMORY", 0.9)

    if _contains_any(text, ("약속", "내일", "나중에", "다음에", "같이 하자")):
        _add(scores, "PROMISE", 0.72)

    if _contains_any(text, ("뭐해", "뭐함", "뭐 하고 있어", "뭐 하고 있었어", "기다렸어", "기다렸지")):
        _add(scores, "WAITING", 0.88)
        _add(scores, "CHAT", 0.45)

    if _contains_any(text, ("서운", "삐졌", "섭섭", "흥", "왜 안", "기다렸잖아")):
        _add(scores, "COMPLAINT", 0.86)

    if _contains_any(text, ("좋은 일", "성공", "붙었어", "합격", "해냈어", "됐다", "됐어", "완성", "끝냈어")):
        _add(scores, "GOODNEWS", 0.84)
        _add(scores, "EXCITED", 0.45)

    if _contains_any(text, ("뭐야", "헐", "진짜?", "진짜야", "어?", "엥", "깜짝")):
        _add(scores, "SURPRISE", 0.72)

    if _contains_any(text, ("미안", "미안해", "죄송", "잘못했어")):
        _add(scores, "APOLOGY", 0.88)
        _add(scores, "AFFECTION", 0.35)

    if _contains_any(text, ("걱정", "불안", "무서워", "어떡하지", "어떻게 하지", "긴장", "망했어")):
        _add(scores, "WORRY", 0.9)

    if _contains_any(text, ("슬퍼", "우울", "속상", "힘들어", "지쳤어", "외로워", "아파")):
        _add(scores, "SAD", 0.9)

    if _contains_any(text, ("신나", "기대돼", "빨리", "재밌겠다", "가자", "하자!!!!")):
        _add(scores, "EXCITED", 0.82)

    if _contains_any(text, ("잘자", "잘게", "졸려", "자러", "자야", "잠와")):
        _add(scores, "SLEEPY", 0.9)
        _add(scores, "AFFECTION", 0.5)

    if "?" in text or _contains_any(text, ("왜", "뭐", "어떻게", "언제", "어디", "누구", "할까", "될까")):
        _bump(scores, "QUESTION", 0.52)

    if category in GREETING_CATEGORIES and max(scores.values()) < 0.62:
        _add(scores, "CHAT", 0.5)
    elif category == "affection_longing":
        _add(scores, "LONGING", 0.9)
        _add(scores, "AFFECTION", 0.62)
    elif category == "compliment":
        _add(scores, "PRAISE", 0.86)
    elif category == "project":
        _add(scores, "PROJECT", 0.86)
    elif category == "comfort":
        _add(scores, "WORRY", 0.65)
    elif category == "conversation_status":
        _add(scores, "WAITING", 0.86)

    if max(scores.values()) <= 0.0:
        scores["CHAT"] = 0.55

    return _clean_scores(scores)


def _clean_scores(scores):
    return {
        key: round(value, 2)
        for key, value in sorted(scores.items(), key=lambda item: item[1], reverse=True)
        if value > 0.0
    }


def top_context(scores):
    if not scores:
        return "CHAT"
    return max(scores.items(), key=lambda item: item[1])[0]


def secondary_context(scores):
    if not scores or len(scores) < 2:
        return None
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)[1][0]


def context_lock(scores, current_category="default"):
    primary = top_context(scores)
    secondary = secondary_context(scores)
    locked_category = CONTEXT_CATEGORY_LOCK.get(primary, current_category)
    locked_life_context = CONTEXT_LIFE_LOCK.get(primary)
    return {
        "primary": primary,
        "secondary": secondary,
        "category": locked_category,
        "life_context": locked_life_context,
        "locked": primary not in ("CHAT",) and scores.get(primary, 0.0) >= 0.62,
    }


def voice_category_for_lock(lock, fallback="default"):
    primary = (lock or {}).get("primary")
    if primary in ("LONGING", "AFFECTION"):
        return "affection_longing"
    if primary == "PRAISE":
        return "compliment"
    if primary == "REPORT":
        return "report"
    if primary == "PROJECT":
        return "project"
    if primary == "GAME":
        return "game"
    if primary == "MUSIC":
        return "music"
    if primary == "FOOD":
        return "food"
    if primary in ("WORRY", "SAD", "APOLOGY", "SLEEPY"):
        return "comfort"
    if primary == "WAITING":
        return "conversation_status"
    if primary == "COMPLAINT":
        return "sulking"
    if primary == "GOODNEWS":
        return "happy"
    if primary in ("SURPRISE", "EXCITED"):
        return "excited"
    return fallback


def describe_context(scores):
    if not scores:
        return ""
    return ", ".join(f"{name}:{score:.2f}" for name, score in list(scores.items())[:4])
