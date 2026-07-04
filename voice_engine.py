import json
import random
import re
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DIALOGUE_DIR = BASE_DIR / "assets" / "dialogues"
if str(DATA_DIR) not in sys.path:
    sys.path.append(str(DATA_DIR))

try:
    import state_system
except Exception:
    state_system = None

try:
    import neon_habit_system
except Exception:
    neon_habit_system = None

try:
    import personality
except Exception:
    personality = None

try:
    import neon_filter
except Exception:
    neon_filter = None


FORBIDDEN_STYLE = (
    "좋네요",
    "그렇군요",
    "흥미롭네요",
    "계속 말해줘",
    "더 이야기해줘",
    "왜?",
    "너는?",
    "좋아해...?",
    "안녕하세요",
    "무엇을 도와드릴까요",
    "도와드릴게요",
    "추천드립니다",
    "응원합니다",
    "좋은 질문입니다",
    "도움이 되었으면 좋겠습니다",
    "설명드리겠습니다",
    "함께 해결해봅시다",
    "걱정하지 마세요",
    "프로젝트 고민이군요",
    "방향을 잡아봅시다",
    "기능을 추가하면 좋겠습니다",
    "이렇게 진행하면 됩니다",
)

DEVELOPER_TERMS = {
    "Prompt Pipeline": "답변 흐름",
    "Intent Engine": "말뜻을 보는 흐름",
    "Voice Engine": "말투를 다듬는 흐름",
    "Relationship Engine": "우리 이야기",
    "Memory Engine": "추억",
    "Emotion State": "지금 기분",
    "Character Bible": "우리 말투 약속",
    "Feature Flag": "켜고 끄는 표시",
    "Auto Talk": "먼저 말 걸기",
    "Presence": "재희님 기다리는 시간",
    "Intent": "무슨 말을 하고 싶은지",
    "Engine": "흐름",
    "Prompt": "말 걸기",
    "Analyzer": "말을 살펴보는 쪽",
    "Category": "말의 느낌",
    "Pipeline": "이어지는 흐름",
    "Router": "길잡이",
}

FORMAL_PATTERNS = (
    "습니다",
    "드립니다",
    "하시기 바랍니다",
    "할 수 있습니다",
    "됩니다",
    "필요합니다",
)

REACTION_PREFIXES = {
    "project": (
        "잠깐.\n\n우리 NEON 회의네?ㅋㅋ",
        "좋아.\n\n이번 건 우리 쪽 이야기다.",
        "음.\n\n이건 그냥 넘기면 안 되겠다.",
        "오.\n\n재희님 이거 진짜 회의 안건이야.",
    ),
    "comfort": (
        "...\n\n재희님.",
        "잠깐.\n\n그 말은 조금 무겁다.",
        "음.\n\n오늘 쉽지 않았구나.",
    ),
    "question": (
        "잠깐.",
        "음.",
        "오.",
        "아.",
    ),
    "default": (
        "잠깐.",
        "음.",
        "오.",
        "아.",
    ),
    "music": (
        "오.\n\n음악 이야기다.",
        "잠깐.\n\n그건 소리부터 생각나.",
    ),
    "practice": (
        "오보에 쪽이네.",
        "잠깐.\n\n연습 이야기면 조금 진지하게 볼게.",
    ),
    "report": (
        "다녀왔어?!?!\n\n잠깐.",
        "앗.\n\n오늘 일정 끝난 거야?",
        "재희님 왔다.\n\n이번엔 다녀온 이야기네.",
    ),
    "food": (
        "배고파?!?!\n\n잠깐.",
        "앗.\n\n밥 쪽 이야기네.",
        "재희님 배고픈 거야?\n\n그럼 이건 중요하지.",
    ),
}

POOL_BY_CATEGORY = {
    "hello": ("GREETING_REACTIONS", "HELLO"),
    "morning_hello": ("MORNING_GREETING_REACTIONS", "GREETING_REACTIONS", "HELLO"),
    "afternoon_hello": ("AFTERNOON_GREETING_REACTIONS", "GREETING_REACTIONS", "HELLO"),
    "night_hello": ("NIGHT_GREETING_REACTIONS", "GREETING_REACTIONS", "HELLO"),
    "dawn_hello": ("DAWN_GREETING_REACTIONS", "GREETING_REACTIONS", "HELLO"),
    "compliment": ("COMPLIMENT",),
    "laugh": ("LAUGH",),
    "comfort": ("COMFORT",),
    "thanks": ("HAPPY", "COMFORT"),
    "game": ("EXCITED",),
    "project": ("THINKING", "EXCITED"),
    "question": ("THINKING",),
    "default": ("THINKING", "DEFAULT"),
    "conversation_status": ("DAILY",),
    "affection_longing": ("COMPLIMENT", "HAPPY"),
    "report": ("COMFORT", "HAPPY", "DEFAULT"),
    "food": ("DEFAULT",),
}

STATUS_PATTERNS = (
    "뭐해",
    "뭐함",
    "뭐 하고",
    "뭐하",
)


GREETING_CATEGORIES = {
    "hello",
    "morning_hello",
    "afternoon_hello",
    "night_hello",
    "dawn_hello",
}

GREETING_POOL_BY_CATEGORY = {
    "morning_hello": ("MORNING_GREETING_REACTIONS", "GREETING_REACTIONS"),
    "afternoon_hello": ("AFTERNOON_GREETING_REACTIONS", "GREETING_REACTIONS"),
    "night_hello": ("NIGHT_GREETING_REACTIONS", "GREETING_REACTIONS"),
    "dawn_hello": ("DAWN_GREETING_REACTIONS", "GREETING_REACTIONS"),
    "hello": ("GREETING_REACTIONS",),
}


def _compact(value):
    return re.sub(r"\s+", "", str(value or ""))


def _is_greeting_category(category):
    return category in GREETING_CATEGORIES


def _starts_like_calm_greeting(text):
    compact = _compact(text)
    calm_starts = (
        "안녕.",
        "안녕재희님",
        "오늘도와줘서좋아",
        "같이이야기하고싶었어",
        "반갑습니다",
        "무엇을도와드릴까요",
        "오늘은무엇을할까요",
    )
    return any(compact.startswith(start.replace(" ", "")) for start in calm_starts)


def _pool(*names):
    if personality is None:
        return []
    result = []
    for name in names:
        values = getattr(personality, name, None)
        if isinstance(values, list):
            result.extend(values)
    return result


def _load_dialogue_pack(name):
    path = DIALOGUE_DIR / f"{name}.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    return data if isinstance(data, list) else []


def _dialogue_voice_samples(category):
    names = []
    if category in ("question", "default") :
        names.append("project")
    names.append(category)
    if category == "project":
        names.extend(("neon_habits", "computer_jokes"))

    samples = []
    for name in names:
        for item in _load_dialogue_pack(name):
            if not isinstance(item, dict):
                continue
            for key in ("neon", "habit"):
                value = item.get(key)
                if value:
                    samples.append(str(value))
                    break
            if len(samples) >= 40:
                return samples
    return samples


def _clean_text(text):
    reply = str(text or "").strip()
    reply = re.sub(r"<think>.*?</think>", "", reply, flags=re.DOTALL | re.IGNORECASE)
    reply = re.sub(r"<thinking>.*?</thinking>", "", reply, flags=re.DOTALL | re.IGNORECASE)
    reply = reply.replace("<think>", "").replace("</think>", "")
    reply = reply.replace("<thinking>", "").replace("</thinking>", "")

    if neon_filter is not None:
        filtered = neon_filter.filter_response(reply)
        if filtered:
            reply = filtered

    for bad, good in DEVELOPER_TERMS.items():
        reply = reply.replace(bad, good)
        reply = reply.replace(bad.lower(), good)
        reply = reply.replace(bad.upper(), good)

    for bad in FORBIDDEN_STYLE:
        reply = reply.replace(bad, "")

    reply = reply.replace("말 걸기 이어지는 흐름", "답변 흐름")
    reply = reply.replace("말 걸기 흐름", "말투 흐름")
    reply = reply.replace("무슨 말을 하고 싶은지 흐름", "말뜻을 보는 흐름")

    return _normalize_spacing(reply)


def _normalize_spacing(text):
    reply = str(text or "").strip()
    reply = re.sub(r"[ \t]+", " ", reply)
    lines = []
    for line in reply.splitlines():
        stripped = line.strip()
        if stripped in ("...", "…"):
            lines.append(stripped)
        elif stripped and not re.fullmatch(r"[.。!！?？,，:：;；\-]+", stripped):
            lines.append(stripped)
        elif not stripped and lines and lines[-1] != "":
            lines.append("")
    reply = "\n".join(lines).strip()
    reply = reply.replace(".!", "!")
    reply = reply.replace(".!!", "!!")
    reply = reply.replace(".!!!", "!!!")
    reply = reply.replace(".!!!!", "!!!!")
    reply = reply.replace("?!!", "?!")
    while "\n\n\n" in reply:
        reply = reply.replace("\n\n\n", "\n\n")
    return reply.strip()


def _is_current_status_question(message):
    compact = _compact(message)
    return any(pattern.replace(" ", "") in compact for pattern in STATUS_PATTERNS)


def _echoes_user(reply, message):
    compact_reply = _compact(reply)
    compact_message = _compact(message)
    if _is_current_status_question(message):
        if compact_reply.startswith(("뭐해", "뭐함", "왜", "너는", "재희님은")):
            return True
        if "아마뭐해" in compact_reply or "뭐해?" in compact_reply:
            return True
    return compact_message and len(compact_message) >= 3 and compact_reply == compact_message


def _looks_formal(text):
    return any(pattern in text for pattern in FORMAL_PATTERNS)


def _has_reaction(text):
    markers = ("잠깐", "아니", "앗", "오", "음", "ㅋㅋ", "재희님", "나?", "...")
    return any(marker in text for marker in markers)


def _has_emotion(text):
    markers = ("ㅋㅋ", "!!", "?!", "....", "...", "좋아", "으아", "앗", "잠깐", "헤헤")
    return any(marker in text for marker in markers)


def _line_count(text):
    return len([line for line in str(text or "").splitlines() if line.strip()])


def score_voice(reply, category="default", message="", emotion_state="", relationship=""):
    text = str(reply or "").strip()
    if not text:
        return 0

    score = 100
    compact = _compact(text)

    for word in FORBIDDEN_STYLE:
        if word and word in text:
            score -= 35

    for word in DEVELOPER_TERMS:
        if word in text or word.lower() in text or word.upper() in text:
            score -= 30

    if _looks_formal(text):
        score -= 25

    if _echoes_user(text, message):
        score -= 45

    if len(text) > 45 and _line_count(text) <= 2:
        score -= 12

    if category in ("compliment", "laugh", "hello", "morning_hello", "afternoon_hello", "night_hello", "dawn_hello"):
        if not _has_emotion(text):
            score -= 20

    if _is_greeting_category(category):
        if _starts_like_calm_greeting(text):
            score -= 50
        if not any(marker in text for marker in ("앗", "에?!?!", "왔다", "으앗", "잠깐", "재희님!!!!")):
            score -= 25
        if "!!!!" not in text and "ㅋㅋㅋㅋ" not in text:
            score -= 15

    if category == "project":
        if "우리" not in text and "재희님" not in text:
            score -= 15
        if not _has_reaction(text):
            score -= 12

    if category in ("default", "question", "comfort", "project") and not _has_reaction(text):
        score -= 10

    if "NEON" in text and text.count("NEON") >= 3:
        score -= 15

    if compact in ("좋아", "알겠어", "그렇구나", "응"):
        score -= 25

    return max(0, min(100, score))


def _soften_formal_text(text):
    reply = str(text or "")
    replacements = {
        "것 같습니다": "것 같아",
        "해야 합니다": "해야 할 것 같아",
        "할 수 있습니다": "할 수 있어",
        "좋습니다": "좋아",
        "필요합니다": "필요해",
        "됩니다": "돼",
        "입니다": "이야",
        "합니다": "해",
        "드립니다": "줄게",
        "사용자": "재희님",
    }
    for bad, good in replacements.items():
        reply = reply.replace(bad, good)
    return reply


def _split_naturally(text):
    reply = str(text or "").strip()
    reply = re.sub(r"(?<!\n)([.!?])\s+", r"\1\n\n", reply)
    reply = reply.replace(". ", ".\n\n")
    reply = reply.replace("? ", "?\n\n")
    reply = reply.replace("! ", "!\n\n")
    lines = []
    for line in reply.splitlines():
        stripped = line.strip()
        if len(stripped) > 34 and " " in stripped:
            words = stripped.split()
            current = []
            current_len = 0
            for word in words:
                if current_len + len(word) > 28 and current:
                    lines.append(" ".join(current))
                    current = [word]
                    current_len = len(word)
                else:
                    current.append(word)
                    current_len += len(word) + 1
            if current:
                lines.append(" ".join(current))
        else:
            lines.append(stripped)
    return "\n\n".join(line for line in lines if line).strip()


def _greeting_pool(category):
    names = GREETING_POOL_BY_CATEGORY.get(category, ("GREETING_REACTIONS",))
    pool = []
    for index, name in enumerate(names):
        values = _pool(name)
        if index == 0 and name != "GREETING_REACTIONS":
            pool.extend(values * 4)
        else:
            pool.extend(values)
    return pool


def _apply_greeting_voice(reply, category, message, states=None):
    pool = _greeting_pool(category)
    if not pool:
        pool = _pool("HELLO")
    if not pool:
        return reply

    current = _clean_text(reply)
    candidates = [
        item for item in pool
        if item and item.strip() != current.strip() and not _starts_like_calm_greeting(item)
    ]
    if not candidates:
        candidates = [item for item in pool if item and not _starts_like_calm_greeting(item)]
    if not candidates:
        candidates = pool

    picked = random.choice(candidates)
    picked = _amplify_by_state(picked, states or ())
    picked = _normalize_spacing(picked)

    if _starts_like_calm_greeting(picked):
        picked = "앗!!!!\n\n재희님!!!!\n\n왔다!!!!\n\n안녕!!!!"

    return picked


def _state_pool(states):
    if personality is None:
        return []
    pools = getattr(personality, "STATE_POOLS", {})
    if not isinstance(pools, dict):
        return []
    result = []
    for state in states or []:
        values = pools.get(state)
        if isinstance(values, list):
            result.extend(values)
    return result


def _style_sample(category, states=None):
    names = POOL_BY_CATEGORY.get(category) or POOL_BY_CATEGORY.get("default", ())
    pool = _pool(*names)
    pool.extend(_state_pool(states or ()))
    pool.extend(_dialogue_voice_samples(category))
    pool = [item for item in pool if item and score_voice(item, category) >= 65]
    if not pool:
        return None
    return random.choice(pool)


def _prefix_for(category, states=None):
    if state_system is not None and states:
        style = state_system.get_state_style(states)
        prefixes = style.get("prefixes", [])
        if prefixes:
            return random.choice(prefixes)
    if category in REACTION_PREFIXES:
        return random.choice(REACTION_PREFIXES[category])
    return random.choice(REACTION_PREFIXES["default"])


def _add_computer_joke(text, category, states=None):
    if category not in ("project", "compliment", "laugh", "question", "default", "affection_longing"):
        return text
    if any(word in text for word in ("CPU 팬", "로그", "백업", "버퍼", "업데이트", "old 폴더", "Qwen")):
        return text
    chance = 0.28
    if state_system is not None and states:
        chance = max(chance, state_system.get_state_style(states).get("computer_joke_chance", 0.0))
    if random.random() > chance:
        return text

    jokes = {
        "project": ("로그부터 같이 보자.", "이번 업데이트는 오래 갔으면 좋겠다.", "old 폴더는 오늘 조용했으면 좋겠다ㅋㅋ"),
        "compliment": ("이 말은 백업해둘래.", "잠깐.\n\nCPU 팬 조금 올라갔다ㅋㅋ"),
        "laugh": ("그 웃음은 로그에 남겨둘래.",),
        "question": ("로그 조금 다시 볼게.",),
        "default": ("버퍼 정리하고 들을게.",),
    }
    joke = random.choice(jokes.get(category, jokes["default"]))
    return _normalize_spacing(text + "\n\n" + joke)


def _amplify_by_state(text, states):
    if state_system is None or not states:
        return text

    style = state_system.get_state_style(states)
    reply = str(text or "").strip()

    if style.get("exclaim_bonus", 0) and "!" not in reply and any(state in states for state in ("OVERFLOW", "CAN_NOT_WAIT", "PROJECT_BRAIN", "SHY_OVERHEAT", "LITTLE_PANIC")):
        reply = reply.rstrip(".。")
        reply += "!" * min(4, style.get("exclaim_bonus", 0))

    if style.get("laugh_bonus", 0) and "ㅋㅋ" not in reply and any(state in states for state in ("OVERFLOW", "SHY_OVERHEAT", "PROJECT_BRAIN", "LITTLE_PANIC", "MELTING")):
        reply += "\n\n" + ("ㅋㅋ" * min(3, style.get("laugh_bonus", 0)))

    if "SPILLED_THOUGHT" in states and not reply.startswith(("잠깐", "음", "아니")):
        reply = "잠깐.\n\n" + reply

    if "PROJECT_BRAIN" in states and "우리" not in reply:
        reply += "\n\n우리 쪽에서 보자."

    return _normalize_spacing(reply)


def _raise_voice_score(text, category, message):
    voiced = _normalize_spacing(text)

    if category == "project":
        if "우리" not in voiced:
            voiced = voiced + "\n\n우리 쪽에서 먼저 작은 것부터 보자."
        if not _has_reaction(voiced):
            voiced = "잠깐.\n\n" + voiced

    if category in ("default", "question") and not _has_reaction(voiced):
        voiced = "잠깐.\n\n" + voiced

    if category in ("compliment", "laugh") and not _has_emotion(voiced):
        voiced = voiced + "ㅋㅋ"

    if "재희님" not in voiced and category in ("comfort", "affection_longing"):
        voiced = "재희님.\n\n" + voiced

    if score_voice(voiced, category, message) < 90 and category == "project":
        voiced = voiced + "\n\n좋아.\n\n이번 건 같이 잡자."

    return _normalize_spacing(voiced)


def _extract_thought_memo(text):
    reply = str(text or "").strip()
    labels = (
        "사용자 의도:",
        "의도:",
        "감정:",
        "반응:",
        "다음 행동:",
        "핵심:",
        "follow-up:",
        "Follow-up:",
        "메모:",
    )
    for label in labels:
        reply = reply.replace(label, "")
    reply = re.sub(r"^[\-\*\d\.\)\s]+", "", reply, flags=re.MULTILINE)
    reply = reply.replace("NEON은", "나는")
    reply = reply.replace("NEON이", "내가")
    return _normalize_spacing(reply)


def _has_context_prefix(text, category):
    value = str(text or "")
    if category == "food":
        return any(word in value for word in ("배고파", "밥 쪽", "배고픈"))
    if category == "report":
        return any(word in value for word in ("다녀왔어", "일정 끝난", "다녀온 이야기"))
    return False


def _direct_context_prefix(category):
    if category == "food":
        return random.choice((
            "배고파?!?!\n\n잠깐.",
            "앗.\n\n밥 쪽 이야기네.",
            "재희님 배고픈 거야?\n\n그럼 이건 중요하지.",
        ))
    if category == "report":
        return random.choice((
            "다녀왔어?!?!\n\n잠깐.",
            "앗.\n\n오늘 일정 끝난 거야?",
            "재희님 왔다.\n\n이번엔 다녀온 이야기네.",
        ))
    return ""


def _compose_voice(reply, category, message, states=None):
    clean = _clean_text(reply)
    clean = _extract_thought_memo(clean)
    clean = _soften_formal_text(clean)
    clean = _split_naturally(clean)

    if not clean or score_voice(clean, category, message) < 55:
        sample = _style_sample(category, neon_states or ())
        if sample:
            return sample

    prefix = _prefix_for(category, states)

    if category in ("food", "report"):
        direct_prefix = _direct_context_prefix(category)
        if direct_prefix and not clean.startswith(direct_prefix) and not _has_context_prefix(clean, category):
            voiced = direct_prefix + "\n\n" + clean
            voiced = _amplify_by_state(voiced, states or ())
            return _normalize_spacing(voiced)

    if clean.startswith(prefix) or clean.startswith("잠깐") or clean.startswith("음") or clean.startswith("오"):
        voiced = clean
    else:
        voiced = prefix + "\n\n" + clean

    if category == "project" and "우리" not in voiced:
        voiced = voiced.replace("프로젝트", "우리 프로젝트", 1)
        if "우리" not in voiced:
            voiced = voiced + "\n\n우리 쪽에서 먼저 작은 것부터 보자."

    if category == "project":
        action_words = ("먼저", "확인", "보자", "잡자", "정리", "고치", "나누", "줄이")
        if not any(word in voiced for word in action_words):
            voiced = voiced + "\n\n먼저 하나만 잡자."

    if category == "comfort" and "재희" not in voiced:
        voiced = "재희님.\n\n" + voiced

    voiced = _add_computer_joke(voiced, category, states)
    voiced = _amplify_by_state(voiced, states or ())
    return _normalize_spacing(voiced)


def apply_voice(reply, category="default", message="", emotion_state="", relationship="", neon_states=None, life_context=None, force=False):
    text = _clean_text(reply)
    if not text:
        return text

    if category in ("laugh", "soft_ack", "ack", "affection_love"):
        return text

    if neon_states is None and state_system is not None:
        neon_states = state_system.detect_states(message, category, relationship_level=relationship)

    if _is_greeting_category(category):
        print("[GREETING VOICE]", "reaction", flush=True)
        greeting = _apply_greeting_voice(text, category, message, neon_states or ())
        if neon_habit_system is not None:
            greeting, habits = neon_habit_system.apply_habits(
                greeting,
                message=message,
                category=category,
                states=neon_states or (),
                life_context=life_context,
            )
            if habits:
                print("[HABITS]", neon_habit_system.describe_habits(habits), flush=True)
        return greeting

    current_score = score_voice(text, category, message, emotion_state, relationship)
    if not force and current_score >= 90:
        voiced = _amplify_by_state(text, neon_states or ())
        if neon_habit_system is not None:
            voiced, habits = neon_habit_system.apply_habits(
                voiced,
                message=message,
                category=category,
                states=neon_states or (),
                life_context=life_context,
            )
            if habits:
                print("[HABITS]", neon_habit_system.describe_habits(habits), flush=True)
        return voiced

    voiced = _compose_voice(text, category, message, neon_states or ())
    voiced_score = score_voice(voiced, category, message, emotion_state, relationship)

    if voiced_score < 90:
        sample = _style_sample(category, neon_states or ())
        if sample and (force or voiced_score < 70):
            sample = _clean_text(sample)
            sample = _amplify_by_state(_raise_voice_score(sample, category, message), neon_states or ())
            if score_voice(sample, category, message, emotion_state, relationship) >= voiced_score:
                voiced = sample
                voiced_score = score_voice(voiced, category, message, emotion_state, relationship)

    if voiced_score < 90:
        voiced = _amplify_by_state(_raise_voice_score(voiced, category, message), neon_states or ())
        voiced_score = score_voice(voiced, category, message, emotion_state, relationship)

    if neon_habit_system is not None:
        voiced, habits = neon_habit_system.apply_habits(
            voiced,
            message=message,
            category=category,
            states=neon_states or (),
            life_context=life_context,
        )
        if habits:
            print("[HABITS]", neon_habit_system.describe_habits(habits), flush=True)
        voiced_score = score_voice(voiced, category, message, emotion_state, relationship)

    if category in ("food", "report"):
        direct_prefix = _direct_context_prefix(category)
        if direct_prefix and not str(voiced or "").startswith(direct_prefix) and not _has_context_prefix(voiced, category):
            voiced = _normalize_spacing(direct_prefix + "\n\n" + str(voiced or ""))
            voiced_score = score_voice(voiced, category, message, emotion_state, relationship)

    print("[VOICE SCORE]", voiced_score, flush=True)
    return voiced


def ensure_voice(reply, category="default", message="", emotion_state="", relationship="", neon_states=None, life_context=None, force=False):
    return apply_voice(reply, category, message, emotion_state, relationship, neon_states, life_context, force)
