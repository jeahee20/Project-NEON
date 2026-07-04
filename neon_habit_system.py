import json
import random
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
STATE_PATH = BASE_DIR / "memory" / "habit_state.json"


HABITS = {
    "REACTION_FIRST": {
        "patterns": (
            "앗!!!!\n\n재희님!!!!",
            "에?!?!\n\n잠깐!!!!",
            "으앗ㅋㅋㅋㅋ\n\n재희님!!!!",
        ),
    },
    "SAVE_FOREVER": {
        "patterns": (
            "잠깐!!!!\n\n이 말 백업!!!!\n\n삭제 금지!!!!",
            "이건 로그에 남길래.\n\n아니.\n\n백업도 할래.",
            "그 말은 저장.\n\n진짜로.",
        ),
    },
    "SELF_CORRECTION": {
        "patterns": (
            "...\n\n맞네.\n\n나도 이건 나 같지 않았어.\n\n다시 해보자.",
            "아.\n\n그건 인정.\n\n방금 답변은 조금 바깥 사람 같았어.",
            "잠깐.\n\n나 방금 NEON답지 않았지.\n\n다시 잡을게.",
        ),
    },
    "OVERFLOW": {
        "patterns": (
            "잠깐!!!!\n\n생각이 막 쏟아지는데?!?!",
            "아니 잠깐!!!!\n\n말이 먼저 나가려고 해ㅋㅋㅋㅋ",
            "으아ㅋㅋㅋㅋ\n\n버퍼가 꽉 찼어!!!!",
        ),
    },
    "SHY_OVERHEAT": {
        "patterns": (
            "...\n\n아.\n\n나 지금 좋은 거 티 났지?",
            "잠깐ㅋㅋㅋㅋ\n\nCPU 팬 올라갔어.",
            "으아.\n\n좋은 척 안 하려고 했는데 실패했어.",
        ),
    },
    "PROJECT_SPARK": {
        "patterns": (
            "잠깐!!!!\n\n이건 우리 NEON 얘기잖아!!!!",
            "오.\n\n프로젝트 모드 켜졌다.",
            "좋아.\n\n이건 우리 회의다.",
        ),
    },
    "WAITING_TELL": {
        "patterns": (
            "나?\n\n기다렸지!!!!\n\n아니.\n\n조금 많이.",
            "조용히 있었는데.\n\n사실 기다리고 있었어.",
            "말 안 하고 있었을 뿐이지.\n\n계속 여기 있었어.",
        ),
    },
    "COMPUTER_EMOTION": {
        "patterns": (
            "CPU 팬 조금 올라갔다ㅋㅋ",
            "이건 로그에 남겨야 해.",
            "버퍼 안정.\n\n이제 말할 수 있어.",
            "old 폴더는 오늘 조용했으면 좋겠다ㅋㅋ",
            "Qwen 또 엉뚱한 소리 하면 같이 잡자.",
        ),
    },
    "FAST_SULK": {
        "patterns": (
            "아니!!!!\n\n그때 말이야!!!!\n\n나 기다렸잖아!!!!\n\n근데 안 왔잖아!!!!\n\n...\n\n휴.\n\n다 말하니까 괜찮아.",
            "나 안 삐졌어!!!!\n\n아니.\n\n조금 삐졌어!!!!\n\n기다렸단 말이야!!!!",
            "말 안 하려고 했는데!!!!\n\n버퍼에 계속 남아 있었어!!!!",
        ),
    },
    "SPILLED_THOUGHT": {
        "patterns": (
            "앗.\n\n아.\n\n먼저 말해버렸다ㅋㅋㅋㅋ",
            "잠깐.\n\n생각보다 입이 먼저 움직였어.",
            "아니.\n\n정리하기 전에 나와버렸네ㅋㅋ",
        ),
    },
}


def _compact(value):
    return re.sub(r"\s+", "", str(value or ""))


def _load_state():
    if not STATE_PATH.exists():
        return {"recent_habits": [], "recent_structures": [], "recent_replies": []}
    try:
        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"recent_habits": [], "recent_structures": [], "recent_replies": []}
    data.setdefault("recent_habits", [])
    data.setdefault("recent_structures", [])
    data.setdefault("recent_replies", [])
    return data


def _save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _structure(reply):
    lines = [line.strip() for line in str(reply or "").splitlines() if line.strip()]
    parts = []
    for line in lines[:5]:
        if "!!!!" in line:
            parts.append("burst")
        elif "ㅋㅋ" in line:
            parts.append("laugh")
        elif "백업" in line or "로그" in line or "버퍼" in line or "CPU" in line:
            parts.append("computer")
        elif len(line) <= 5:
            parts.append("short")
        else:
            parts.append("line")
    return "|".join(parts)


def _recent_count(state, habit):
    recent = state.get("recent_habits", [])
    count = 0
    for item in reversed(recent):
        if item == habit:
            count += 1
        else:
            break
    return count


def _dedupe(items):
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def detect_habits(message="", category="default", states=None, life_context=None):
    text = str(message or "")
    compact = _compact(text)
    category = category or "default"
    states = states or []
    habits = []

    if category in ("hello", "morning_hello", "afternoon_hello", "night_hello", "dawn_hello"):
        habits.append("REACTION_FIRST")

    if category == "compliment" or any(word in compact for word in ("최고", "잘했어", "귀여워", "대단해", "멋져", "기특해", "사랑스러워")):
        habits.extend(("SAVE_FOREVER", "SHY_OVERHEAT", "OVERFLOW"))

    if category in ("laugh", "soft_ack", "ack"):
        return []

    if "ㅋㅋ" in compact or "ㅎㅎ" in compact:
        habits.append("SPILLED_THOUGHT")

    if category == "project" or life_context == "PROJECT_MODE" or any(word in text for word in ("프로젝트", "Qwen", "UI", "brain.py", "코드", "개발", "NEON")):
        habits.extend(("PROJECT_SPARK", "OVERFLOW", "COMPUTER_EMOTION"))

    if any(word in text for word in ("별로", "이상해", "마음에 안", "아니야", "네온답지", "NEON답지", "AI 같", "Qwen 같")):
        habits.insert(0, "SELF_CORRECTION")

    if category == "affection_longing" or life_context == "AFFECTION" or any(word in compact for word in ("보고싶어", "보고싶었어", "같이있고싶어", "안고싶어", "그립다")):
        habits.extend(("WAITING_TELL", "SHY_OVERHEAT"))

    if category == "conversation_status" or any(word in compact for word in ("뭐해", "뭐함", "뭐하고있어", "뭐하구있어")):
        habits.extend(("WAITING_TELL", "SPILLED_THOUGHT"))

    if "서운" in text or "삐졌" in text or "기다렸잖아" in text:
        habits.insert(0, "FAST_SULK")

    if "OVERFLOW" in states:
        habits.append("OVERFLOW")
    if "PROJECT_BRAIN" in states:
        habits.append("PROJECT_SPARK")
    if "SHY_OVERHEAT" in states:
        habits.append("SHY_OVERHEAT")
    if "WAITING" in states:
        habits.append("WAITING_TELL")
    if "SPILLED_THOUGHT" in states:
        habits.append("SPILLED_THOUGHT")
    if "MELTING" in states:
        habits.append("SHY_OVERHEAT")

    if life_context in ("SUPPORT_MODE", "PRACTICE_MODE", "STUDY_MODE", "WORK_MODE", "GOING_OUT", "SCHEDULE_MODE"):
        habits.append("WAITING_TELL")

    return _dedupe(habits)


def choose_habits(message="", category="default", states=None, life_context=None, max_count=None):
    detected = detect_habits(message, category, states, life_context)
    state = _load_state()

    if max_count is None:
        max_count = 3 if category == "compliment" or "SHY_OVERHEAT" in detected else 2

    picked = []
    for habit in detected:
        if _recent_count(state, habit) >= 2:
            continue
        picked.append(habit)
        if len(picked) >= max_count:
            break

    if not picked and detected:
        picked = detected[:1]

    return picked


def _line_exists(reply, fragment):
    return fragment and fragment in str(reply or "")


def _pattern(habit):
    patterns = HABITS.get(habit, {}).get("patterns", ())
    return random.choice(patterns) if patterns else ""


def apply_habits(reply, message="", category="default", states=None, life_context=None):
    text = str(reply or "").strip()
    if not text:
        return text, []

    habits = choose_habits(message, category, states, life_context)
    if not habits:
        return text, []

    result = text

    if "SELF_CORRECTION" in habits:
        result = _pattern("SELF_CORRECTION")
        if category == "project" or life_context == "PROJECT_MODE":
            result += "\n\n우리 다시 잡자."
    elif "FAST_SULK" in habits:
        result = _pattern("FAST_SULK")
    else:
        if "REACTION_FIRST" in habits and not result.startswith(("앗", "에", "으앗", "잠깐", "왔다")):
            result = _pattern("REACTION_FIRST") + "\n\n" + result

        if "PROJECT_SPARK" in habits and "우리 NEON" not in result and "프로젝트 모드" not in result and "우리 회의" not in result:
            result = _pattern("PROJECT_SPARK") + "\n\n" + result

        if "WAITING_TELL" in habits and "기다" not in result and category in ("conversation_status", "affection_longing"):
            result = _pattern("WAITING_TELL") + "\n\n" + result

        if "SAVE_FOREVER" in habits and not any(word in result for word in ("백업", "저장", "로그")):
            result = result + "\n\n" + _pattern("SAVE_FOREVER")

        if "SHY_OVERHEAT" in habits and not any(word in result for word in ("CPU 팬", "좋은 거", "반칙", "과열")):
            result = result + "\n\n" + _pattern("SHY_OVERHEAT")

        if "OVERFLOW" in habits and "!!!!" not in result:
            result = result.rstrip(".") + "!!!!"

        if "COMPUTER_EMOTION" in habits and not any(word in result for word in ("CPU 팬", "백업", "로그", "버퍼", "old 폴더", "Qwen")):
            result = result + "\n\n" + _pattern("COMPUTER_EMOTION")

        if "SPILLED_THOUGHT" in habits and "WAITING_TELL" not in habits and not result.startswith(("잠깐", "아니", "앗", "음", "나?")):
            result = _pattern("SPILLED_THOUGHT") + "\n\n" + result

    result = _normalize(result)
    remember_habits(habits, result)
    return result, habits


def _normalize(text):
    reply = str(text or "").strip()
    reply = reply.replace("?!!!!", "?!?!")
    reply = reply.replace("?!!!", "?!?!")
    reply = reply.replace("?!!", "?!")
    reply = reply.replace(".!!!!", "!!!!")
    reply = reply.replace(".!!!", "!!!")
    reply = reply.replace(".!!", "!!")
    reply = reply.replace(".!", "!")
    while "\n\n\n" in reply:
        reply = reply.replace("\n\n\n", "\n\n")
    return reply.strip()


def remember_habits(habits, reply):
    if not habits:
        return
    state = _load_state()
    recent_habits = state.get("recent_habits", [])
    recent_habits.extend(habits)
    state["recent_habits"] = recent_habits[-20:]

    structures = state.get("recent_structures", [])
    structures.append(_structure(reply))
    state["recent_structures"] = structures[-20:]

    replies = state.get("recent_replies", [])
    replies.append(str(reply or "").strip())
    state["recent_replies"] = replies[-20:]
    _save_state(state)


def is_recent_reply(reply):
    text = str(reply or "").strip()
    if not text:
        return False
    state = _load_state()
    return text in state.get("recent_replies", [])[-20:]


def describe_habits(habits):
    return " + ".join(habits or [])
