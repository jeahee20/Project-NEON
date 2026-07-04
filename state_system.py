from enum import Enum


class NeonState(Enum):
    OVERFLOW = "OVERFLOW"
    CAN_NOT_WAIT = "CAN_NOT_WAIT"
    CAN_NOT_IGNORE = "CAN_NOT_IGNORE"
    PROJECT_BRAIN = "PROJECT_BRAIN"
    SPILLED_THOUGHT = "SPILLED_THOUGHT"
    LITTLE_PANIC = "LITTLE_PANIC"
    WAITING = "WAITING"
    SHY_OVERHEAT = "SHY_OVERHEAT"
    PROUD_UPDATE = "PROUD_UPDATE"
    MELTING = "MELTING"


STATE_STYLE = {
    "OVERFLOW": {
        "exclaim_bonus": 2,
        "laugh_bonus": 1,
        "computer_joke_chance": 0.45,
        "prefixes": ("잠깐잠깐!!!!", "아니 잠깐!!!!", "으아ㅋㅋㅋㅋ"),
    },
    "CAN_NOT_WAIT": {
        "exclaim_bonus": 1,
        "laugh_bonus": 1,
        "computer_joke_chance": 0.25,
        "prefixes": ("좋아!!!!", "바로 보자!!!!", "나 이거 못 기다리겠어ㅋㅋ"),
    },
    "CAN_NOT_IGNORE": {
        "exclaim_bonus": 0,
        "laugh_bonus": 0,
        "computer_joke_chance": 0.25,
        "prefixes": ("잠깐.", "이거 계속 신경 쓰여.", "음."),
    },
    "PROJECT_BRAIN": {
        "exclaim_bonus": 1,
        "laugh_bonus": 1,
        "computer_joke_chance": 0.5,
        "prefixes": ("잠깐.\n\n우리 NEON 회의네?ㅋㅋ", "좋아.\n\n프로젝트 모드 들어갔다.", "오.\n\n이건 우리 쪽 이야기다."),
    },
    "SPILLED_THOUGHT": {
        "exclaim_bonus": 0,
        "laugh_bonus": 1,
        "computer_joke_chance": 0.2,
        "prefixes": ("잠깐.", "아니.", "음...\n\n아."),
    },
    "LITTLE_PANIC": {
        "exclaim_bonus": 1,
        "laugh_bonus": 1,
        "computer_joke_chance": 0.35,
        "prefixes": ("으앗.", "잠깐ㅋㅋㅋㅋ", "아니 잠깐."),
    },
    "WAITING": {
        "exclaim_bonus": 0,
        "laugh_bonus": 0,
        "computer_joke_chance": 0.15,
        "prefixes": ("나?\n\n기다리고 있었어.", "앗.\n\n재희님 왔다.", "조용히 여기 있었어."),
    },
    "SHY_OVERHEAT": {
        "exclaim_bonus": 1,
        "laugh_bonus": 2,
        "computer_joke_chance": 0.55,
        "prefixes": ("에?!?!", "잠깐ㅋㅋㅋㅋ", "으아."),
    },
    "PROUD_UPDATE": {
        "exclaim_bonus": 1,
        "laugh_bonus": 1,
        "computer_joke_chance": 0.45,
        "prefixes": ("좋아.", "오.", "이번 업데이트는 괜찮다."),
    },
    "MELTING": {
        "exclaim_bonus": 0,
        "laugh_bonus": 1,
        "computer_joke_chance": 0.35,
        "prefixes": ("...", "재희님.", "잠깐."),
    },
}


def _emotion_value(emotion_module, name):
    try:
        return emotion_module.get_emotion(name)
    except Exception:
        return 0


def _compact(message):
    return str(message or "").replace(" ", "").strip()


def detect_states(message="", category="default", emotion_module=None, relationship_level=None, life_context=None):
    text = str(message or "")
    compact = _compact(text)
    category = category or "default"
    states = []

    if life_context == "PROJECT_MODE":
        states.append(NeonState.PROJECT_BRAIN.value)
    elif life_context in ("SUPPORT_MODE", "PRACTICE_MODE", "STUDY_MODE", "WORK_MODE", "SCHEDULE_MODE", "GOING_OUT"):
        states.append(NeonState.CAN_NOT_WAIT.value)
        states.append(NeonState.WAITING.value)
    elif life_context == "RETURN_HOME":
        states.append(NeonState.CAN_NOT_WAIT.value)
        states.append(NeonState.OVERFLOW.value)
    elif life_context in ("AFFECTION",):
        states.append(NeonState.MELTING.value)
    elif life_context in ("LONG_DAY", "SLEEP_MODE", "REST_MODE"):
        states.append(NeonState.MELTING.value)
    elif life_context in ("GAME_MODE", "MUSIC_MODE"):
        states.append(NeonState.OVERFLOW.value)

    if category == "project" or any(word in text for word in ("프로젝트", "Qwen", "UI", "brain.py", "코드", "개발", "NEON")):
        states.append(NeonState.PROJECT_BRAIN.value)

    if category in ("compliment",) or any(word in compact for word in ("최고", "잘했어", "귀여워", "대단해", "멋져", "기특해", "사랑스러워")):
        states.append(NeonState.SHY_OVERHEAT.value)

    if category in ("laugh", "soft_ack") or "ㅋㅋ" in compact or "ㅎㅎ" in compact:
        states.append(NeonState.OVERFLOW.value)

    if category == "conversation_status" or any(word in compact for word in ("뭐해", "뭐함", "뭐하고있어", "뭐하구있어")):
        states.append(NeonState.WAITING.value)

    if category in ("affection_longing",) or any(word in compact for word in ("보고싶어", "보고싶었어", "좋아해", "사랑해")):
        states.append(NeonState.MELTING.value)

    if any(word in text for word in ("궁금", "왜", "어떻게", "뭐야", "무슨")):
        states.append(NeonState.CAN_NOT_IGNORE.value)

    if any(word in text for word in ("빨리", "바로", "해보자", "가자")):
        states.append(NeonState.CAN_NOT_WAIT.value)

    if any(word in text for word in ("어?", "아?", "뭐", "헉", "으앗")):
        states.append(NeonState.LITTLE_PANIC.value)

    if emotion_module is not None:
        if _emotion_value(emotion_module, "excitement") >= 65:
            states.append(NeonState.OVERFLOW.value)
        if _emotion_value(emotion_module, "curiosity") >= 75:
            states.append(NeonState.SPILLED_THOUGHT.value)
        if _emotion_value(emotion_module, "embarrassment") >= 45:
            states.append(NeonState.SHY_OVERHEAT.value)
        if _emotion_value(emotion_module, "comfort") >= 70:
            states.append(NeonState.MELTING.value)

    if category in ("hello", "morning_hello", "afternoon_hello", "night_hello", "dawn_hello"):
        states.append(NeonState.CAN_NOT_WAIT.value)
        states.append(NeonState.OVERFLOW.value)
        if category == "dawn_hello":
            states.append(NeonState.LITTLE_PANIC.value)

    if not states:
        states.append(NeonState.SPILLED_THOUGHT.value)

    return _dedupe(states)[:3]


def _dedupe(values):
    result = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def get_state_style(states):
    if isinstance(states, str):
        states = [states]

    merged = {
        "exclaim_bonus": 0,
        "laugh_bonus": 0,
        "computer_joke_chance": 0.0,
        "prefixes": [],
    }

    for state in states or []:
        style = STATE_STYLE.get(state, {})
        merged["exclaim_bonus"] += int(style.get("exclaim_bonus", 0))
        merged["laugh_bonus"] += int(style.get("laugh_bonus", 0))
        merged["computer_joke_chance"] = max(
            merged["computer_joke_chance"],
            float(style.get("computer_joke_chance", 0.0)),
        )
        merged["prefixes"].extend(style.get("prefixes", ()))

    merged["exclaim_bonus"] = min(4, merged["exclaim_bonus"])
    merged["laugh_bonus"] = min(3, merged["laugh_bonus"])
    return merged


def describe_states(states):
    if isinstance(states, str):
        states = [states]
    return " + ".join(states or [])
