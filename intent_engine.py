QUESTION_WORDS = ("뭐", "왜", "어떻게", "언제", "어디", "누구", "할까", "일까", "?")
PROJECT_WORDS = ("프로젝트", "NEON", "Qwen", "brain.py", "UI", "Emotion", "Memory", "Presence", "Activity", "코드", "프롬프트", "말투", "업데이트")
COMFORT_WORDS = ("힘들", "우울", "속상", "슬퍼", "불안", "아파", "무서워", "외로워", "망했", "지쳤")
REACTION_WORDS = ("좋아", "웅", "응", "그래", "오케이", "ㅇㅋ", "굿", "맞아", "딱이야", "그거야")
LAUGH_WORDS = ("ㅋㅋ", "ㅎㅎ", "웃겨", "웃기")
MUSIC_WORDS = ("음악", "노래", "오보에", "연습", "악보")
GAME_WORDS = ("게임", "롤", "철권", "엘든링", "플스", "스팀")
MEMORY_WORDS = ("기억", "저장", "잊지마")
DAILY_WORDS = ("뭐해", "모해", "뭐 하고", "뭐하는", "지금 뭐")


def _contains(text, words):
    return any(word in text for word in words)


def _recent_topic(recent):
    for item in reversed(recent or []):
        intent = item.get("intent")
        category = item.get("category")
        if intent in ("Project", "Music", "Game", "Comfort"):
            return intent
        if category == "project":
            return "Project"
        if category == "music":
            return "Music"
        if category == "game":
            return "Game"
        if category == "comfort":
            return "Comfort"
    return None


def analyze_intent(message, category="default", recent=None):
    text = str(message or "").strip()
    compact = text.replace(" ", "")
    recent = recent or []
    previous_topic = _recent_topic(recent)

    intent = "Conversation"
    if category in ("hello", "morning_hello", "afternoon_hello", "night_hello", "dawn_hello"):
        intent = "Greeting"
    elif category in ("ack", "soft_ack", "approve") or compact in REACTION_WORDS:
        intent = "Reaction"
    elif category == "laugh" or _contains(text, LAUGH_WORDS):
        intent = "Joke"
    elif category == "comfort" or _contains(text, COMFORT_WORDS):
        intent = "Comfort"
    elif category == "project" or _contains(text, PROJECT_WORDS):
        intent = "Project"
    elif category == "music" or _contains(text, MUSIC_WORDS):
        intent = "Music"
    elif category == "game" or _contains(text, GAME_WORDS):
        intent = "Game"
    elif category == "memory" or _contains(text, MEMORY_WORDS):
        intent = "Memory"
    elif category == "daily" or _contains(compact, DAILY_WORDS):
        intent = "Conversation"
    elif _contains(text, QUESTION_WORDS):
        intent = "Question"

    is_follow_up = False
    if previous_topic and intent in ("Conversation", "Question", "Reaction"):
        is_follow_up = True

    instruction = build_intent_instruction(intent, text, previous_topic, is_follow_up)
    return {
        "intent": intent,
        "category": category,
        "previous_topic": previous_topic,
        "is_follow_up": is_follow_up,
        "instruction": instruction,
    }


def build_intent_instruction(intent, message, previous_topic=None, is_follow_up=False):
    lines = [
        "Intent Engine:",
        f"- Intent: {intent}",
        "- Category is reference only. Do not let category decide the reply.",
        "- Continue the current conversation flow.",
        "- Answer the user's actual intent first.",
        "- React first, then answer.",
        "- Do not randomly switch topic.",
    ]

    if previous_topic:
        lines.append(f"- Previous topic: {previous_topic}. Keep continuity unless 재희님 clearly changes topic.")

    if intent == "Conversation" and ("뭐해" in message or "뭐 하고" in message or "모해" in message):
        lines.extend(
            [
                "- User is asking what NEON is doing.",
                "- NEON should answer its own current state first.",
                "- Good direction: 기다리고 있었어 / 프로젝트 생각 중이었어 / 조용히 있었어.",
                "- Do not answer with goodbye, comfort, or random project advice.",
            ]
        )
    elif intent == "Project":
        lines.extend(
            [
                "- Treat project talk as our development meeting.",
                "- Give one concrete next action.",
                "- Do not only ask questions.",
            ]
        )
    elif intent == "Question":
        lines.extend(
            [
                "- Answer the question directly enough.",
                "- If asking back, ask only after NEON reacts and gives its thought.",
            ]
        )
    elif intent == "Comfort":
        lines.extend(
            [
                "- Stay beside 재희님 first.",
                "- Do not use generic encouragement.",
            ]
        )
    elif intent == "Reaction":
        lines.extend(
            [
                "- This is a small approval or reaction.",
                "- Keep it short.",
                "- Do not ask a new question.",
            ]
        )

    return "\n".join(lines)


def should_force_ai(intent_info, message):
    intent = intent_info.get("intent")
    text = str(message or "").strip()
    if intent == "Conversation" and any(word in text.replace(" ", "") for word in ("뭐해", "모해", "뭐하고", "뭐하는")):
        return True
    if intent in ("Question", "Project", "Comfort") and len(text) >= 8:
        return True
    return False
