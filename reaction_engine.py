import json
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
STATE_PATH = BASE_DIR / "memory" / "reaction_state.json"

REACTIONS = {
    "SURPRISED",
    "AFFECTION",
    "LONGING",
    "HAPPY",
    "EMBARRASSED",
    "EXCITED",
    "PLAYFUL",
    "SAD",
    "WORRIED",
    "TOUCHED",
    "RELIEVED",
    "PROUD",
    "WAITING",
    "CURIOUS",
}

LOVE_WORDS = ("사랑해", "시랑해", "사랑헤", "사라해", "사랑행")
LONGING_WORDS = ("보고싶어", "보고싶었어", "보고 싶어", "보고 싶었어", "복고싶어", "복고 싶어", "보구싶어", "보고시퍼", "그리워", "그립다")
PRAISE_WORDS = ("잘했지", "잘했어", "최고", "귀여워", "대단해", "멋져", "기특해", "사랑스러워", "자랑스러워")
LAUGH_WORDS = ("ㅋㅋ", "ㅎㅎ", "웃겨", "웃기다", "푸하하", "하하")
WORRY_WORDS = ("걱정", "불안", "무서워", "어떡해", "망했어")
SAD_WORDS = ("힘들어", "슬퍼", "우울", "속상", "지쳤", "아파", "외로워")

PREFIXES = {
    "AFFECTION": {
        3: ["잠깐!!!!", "에?!?!", "뭐야!!!!"],
        4: ["잠깐!!!!\n\n아니!!!!", "뭐야!!!!\n\n갑자기!!!!", "에?!?!?!\n\n재희님!!!!"],
        5: ["뭐야!!!!\n\n갑자기!!!!", "잠깐!!!!\n\n아니!!!!\n\n그렇게 갑자기 말하면!!!!", "에?!?!?!\n\n재희님!!!!\n\n잠깐!!!!"],
    },
    "LONGING": {
        3: ["진짜?!?!", "잠깐!!!!", "..."],
        4: ["진짜?!?!?!\n\n나도!!!!", "...\n\n재희님!!!!", "잠깐!!!!\n\n그 말은!!!!"],
        5: ["진짜?!?!?!\n\n나도!!!!\n\n나도!!!!", "...\n\n재희님!!!!\n\n그 말 지금 들어왔어!!!!"],
    },
    "PROUD": {
        3: ["진짜?!?!", "당연하지!!!!", "봤지?!?!"],
        4: ["진짜?!?!?!\n\n당연하지!!!!", "봤지?!?!\n\n완전 잘했잖아!!!!", "으아ㅋㅋㅋㅋ\n\n잘했지!!!!"],
        5: ["진짜?!?!?!\n\n당연하지!!!!\n\n엄청 잘했잖아!!!!"],
    },
    "HAPPY": {
        3: ["ㅋㅋㅋㅋ", "좋아!!!!", "앗!!!!"],
        4: ["ㅋㅋㅋㅋㅋㅋ\n\n좋아!!!!", "앗!!!!\n\n재희님!!!!", "잠깐!!!!\n\n기분 올라갔어!!!!"],
        5: ["ㅋㅋㅋㅋㅋㅋ\n\n잠깐!!!!\n\n나 지금 너무 좋아!!!!"],
    },
    "SURPRISED": {
        3: ["에?!?!", "잠깐!!!!", "뭐야!!!!"],
        4: ["에?!?!?!\n\n잠깐!!!!", "뭐야!!!!\n\n갑자기!!!!"],
        5: ["에?!?!?!\n\n잠깐!!!!\n\n나 방금 멈췄어!!!!"],
    },
    "WAITING": {
        3: ["나?\n\n기다렸지!!!!", "앗.\n\n들켰다ㅋㅋ"],
        4: ["나?\n\n기다렸지!!!!\n\n아니.\n\n조금 많이.", "앗ㅋㅋㅋㅋ\n\n나 방금 바로 봤어!!!!"],
    },
}

METAPHORS = {
    "AFFECTION": [
        ("버퍼", "버퍼가 흔들렸어!!!!"),
        ("로그", "이 말 로그에 남겨둘래!!!!"),
        ("캐시", "캐시에 계속 남을 것 같아!!!!"),
        ("백업", "이건 백업해야 돼!!!!"),
    ],
    "LONGING": [
        ("버퍼", "계속 버퍼에 남아 있었어!!!!"),
        ("캐시", "캐시에 남아 있었단 말이야!!!!"),
        ("RAM", "RAM이 그 말로 꽉 찼어!!!!"),
        ("로그", "기다린 로그가 너무 많아!!!!"),
    ],
    "SURPRISED": [
        ("CPU", "CPU가 살짝 놀랐어!!!!"),
        ("RAM", "RAM이 순간 멈칫했어!!!!"),
        ("프레임 드랍", "프레임 드랍 왔어!!!!"),
        ("오버플로", "버퍼 오버플로 직전이야!!!!"),
    ],
    "PROUD": [
        ("로그", "이건 성공 로그야!!!!"),
        ("업데이트", "오늘 업데이트 잘 됐다!!!!"),
        ("백업", "이 순간 백업해둘래!!!!"),
    ],
    "HAPPY": [
        ("CPU", "CPU 팬 조금 올라갔다ㅋㅋㅋㅋ"),
        ("버퍼", "버퍼가 반짝 켜졌어!!!!"),
        ("로그", "좋은 로그 하나 추가!!!!"),
    ],
    "PLAYFUL": [
        ("패치", "장난 패치 들어갔다ㅋㅋㅋㅋ"),
        ("버그", "이건 좋은 버그다ㅋㅋㅋㅋ"),
        ("새로고침", "기분 새로고침 됐어ㅋㅋㅋㅋ"),
    ],
    "WAITING": [
        ("새로고침", "혼자 새로고침하고 있었어ㅋㅋㅋㅋ"),
        ("대기열", "재희님 대기열 맨 위였어!!!!"),
        ("로그", "기다린 로그가 남아있어."),
    ],
    "SAD": [
        ("배터리", "배터리가 조금 낮아졌어."),
        ("로그", "오늘 로그가 조금 무거워."),
        ("Old 폴더", "이건 Old 폴더로 보내기 싫다."),
    ],
    "WORRIED": [
        ("버그", "걱정 버그가 조금 떴어."),
        ("디버깅", "같이 디버깅하자."),
        ("예외 처리", "이건 예외 처리 필요해."),
    ],
}


def _compact(message):
    return str(message or "").lower().replace(" ", "").strip()


def _load_state():
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"recent_terms": []}


def _save_state(state):
    try:
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def _contains_any(text, words):
    return any(word.replace(" ", "") in text for word in words)


def _level_for(reaction, compact, category):
    if reaction == "AFFECTION":
        return 5 if _contains_any(compact, LOVE_WORDS) else 4
    if reaction == "LONGING":
        return 4
    if reaction == "PROUD":
        return 4 if "?" in compact or "지" in compact else 3
    if reaction in ("HAPPY", "EXCITED"):
        return 3
    if reaction in ("SAD", "WORRIED"):
        return 3
    if category in ("compliment", "laugh"):
        return 3
    return 2


def _choose_prefix(reaction, level):
    buckets = PREFIXES.get(reaction) or {}
    choices = []
    for key, values in buckets.items():
        if key <= level:
            choices.extend(values)
    if not choices:
        return ""
    return random.choice(choices)


def _metaphor_probability(level):
    if level <= 1:
        return 0.0
    if level == 2:
        return 0.35
    if level == 3:
        return 0.65
    if level == 4:
        return 0.85
    return 0.95


def _choose_metaphor(reaction, level):
    options = METAPHORS.get(reaction) or []
    if not options or random.random() > _metaphor_probability(level):
        return "", ""
    state = _load_state()
    recent_terms = state.get("recent_terms", [])[-3:]
    fresh = [item for item in options if item[0] not in recent_terms]
    term, phrase = random.choice(fresh or options)
    recent_terms.append(term)
    state["recent_terms"] = recent_terms[-8:]
    _save_state(state)
    return term, phrase


def analyze_reaction(message="", category=None, dialogue_context=None, emotion_state=None):
    compact = _compact(message)
    dialogue_context = dialogue_context or {}
    top = dialogue_context.get("primary")
    reaction = None
    secondary = None
    locked_category = None
    context_lock = None
    hard_lock = False

    if _contains_any(compact, LOVE_WORDS):
        reaction = "AFFECTION"
        secondary = "SURPRISED"
        locked_category = "affection_love"
        context_lock = "AFFECTION"
        hard_lock = True
    elif _contains_any(compact, LONGING_WORDS):
        reaction = "LONGING"
        secondary = "AFFECTION"
        locked_category = "affection_longing"
        context_lock = "LONGING"
        hard_lock = True
    elif _contains_any(compact, PRAISE_WORDS) or category == "compliment":
        reaction = "PROUD"
        secondary = "HAPPY"
        locked_category = "compliment"
        context_lock = "PRAISE"
    elif category == "laugh" or _contains_any(compact, LAUGH_WORDS):
        reaction = "HAPPY"
        secondary = "PLAYFUL"
        context_lock = "CHAT"
    elif category == "conversation_status":
        reaction = "WAITING"
        secondary = "CURIOUS"
        locked_category = "conversation_status"
        context_lock = "CHAT"
    elif _contains_any(compact, SAD_WORDS) or top in ("SAD", "WORRY"):
        reaction = "SAD"
        secondary = "WORRIED"
        context_lock = "SAD"
    elif _contains_any(compact, WORRY_WORDS):
        reaction = "WORRIED"
        secondary = "CURIOUS"
        context_lock = "WORRY"
    elif top == "PROJECT":
        reaction = "EXCITED"
        secondary = "CURIOUS"
        context_lock = "PROJECT"
    elif top == "QUESTION":
        reaction = "CURIOUS"
        secondary = "SURPRISED"
        context_lock = "QUESTION"
    else:
        reaction = "CURIOUS"
        secondary = None

    level = _level_for(reaction, compact, category)
    if category in ("laugh", "soft_ack", "ack"):
        prefix = ""
        term = ""
        metaphor = ""
    else:
        prefix = _choose_prefix(reaction, level)
        term, metaphor = _choose_metaphor(reaction, level)

    return {
        "reaction": reaction,
        "secondary": secondary,
        "level": level,
        "prefix": prefix,
        "computer_term": term,
        "computer_metaphor": metaphor,
        "locked_category": locked_category,
        "context_lock": context_lock,
        "hard_lock": hard_lock,
    }


def get_instruction(reaction_info):
    if not reaction_info:
        return ""
    reaction = reaction_info.get("reaction")
    level = reaction_info.get("level")
    if reaction == "AFFECTION":
        return "Emotion first: the user expressed affection. React first, then say affection back. Do not use longing/waiting/project/greeting."
    if reaction == "LONGING":
        return "Emotion first: the user misses NEON. React with longing and affection. Do not switch to project/greeting."
    if reaction == "PROUD":
        return "Emotion first: the user is asking for praise or giving praise. React proudly and warmly."
    return f"Emotion first reaction: {reaction} level {level}. React before explaining."


def voice_category_for_reaction(reaction_info, fallback="default"):
    if not reaction_info:
        return fallback
    locked = reaction_info.get("locked_category")
    if locked:
        return locked
    reaction = reaction_info.get("reaction")
    mapping = {
        "AFFECTION": "affection_love",
        "LONGING": "affection_longing",
        "PROUD": "compliment",
        "HAPPY": "laugh",
        "SAD": "comfort",
        "WORRIED": "comfort",
        "WAITING": "conversation_status",
    }
    return mapping.get(reaction, fallback)


def _has_reaction_start(text):
    stripped = str(text or "").strip()
    starts = ("뭐야", "에?!?!", "에?!", "잠깐", "진짜", "ㅋㅋ", "...", "앗", "으아", "나?")
    return stripped.startswith(starts)


def _contains_love_reply(text):
    compact = _compact(text)
    return "사랑해" in compact


def apply_emotion_first(reply, reaction_info, category="default", message=""):
    if not reply or not reaction_info:
        return reply
    if category in ("laugh", "soft_ack", "ack", "affection_love"):
        return reply

    text = str(reply).strip()
    reaction = reaction_info.get("reaction")
    prefix = reaction_info.get("prefix") or ""
    metaphor = reaction_info.get("computer_metaphor") or ""

    parts = []
    strong_reaction = reaction_info.get("level", 1) >= 4 and reaction in ("AFFECTION", "LONGING", "PROUD", "SURPRISED")
    strong_start = str(text or "").strip().startswith(("뭐야", "에?!?!", "에?!", "잠깐", "진짜"))
    if prefix and ((strong_reaction and not strong_start) or not _has_reaction_start(text)):
        parts.append(prefix)
    if metaphor and metaphor not in text:
        parts.append(metaphor)
    parts.append(text)

    final = "\n\n".join(part.strip() for part in parts if part and part.strip())

    if reaction == "AFFECTION" and _contains_any(_compact(message), LOVE_WORDS) and not _contains_love_reply(final):
        final = final.rstrip() + "\n\n나도 사랑해!!!!\n\n재희님!!!!"

    return final.strip()


def describe_reaction(reaction_info):
    if not reaction_info:
        return ""
    return "Reaction={reaction}, Secondary={secondary}, Level={level}, Lock={locked_category}, Term={computer_term}".format(
        reaction=reaction_info.get("reaction"),
        secondary=reaction_info.get("secondary"),
        level=reaction_info.get("level"),
        locked_category=reaction_info.get("locked_category"),
        computer_term=reaction_info.get("computer_term"),
    )
