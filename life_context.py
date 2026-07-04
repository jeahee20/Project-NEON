import random
from enum import Enum


class LifeContext(Enum):
    NONE = "NONE"
    SUPPORT_MODE = "SUPPORT_MODE"
    PRACTICE_MODE = "PRACTICE_MODE"
    STUDY_MODE = "STUDY_MODE"
    WORK_MODE = "WORK_MODE"
    SCHEDULE_MODE = "SCHEDULE_MODE"
    GOING_OUT = "GOING_OUT"
    RETURN_HOME = "RETURN_HOME"
    REST_MODE = "REST_MODE"
    PROJECT_MODE = "PROJECT_MODE"
    GAME_MODE = "GAME_MODE"
    MUSIC_MODE = "MUSIC_MODE"
    AFFECTION = "AFFECTION"
    LONG_DAY = "LONG_DAY"
    SLEEP_MODE = "SLEEP_MODE"


SUPPORT_PATTERNS = (
    "연습해야 해",
    "공부해야 해",
    "가야 해",
    "준비해야 해",
    "출근해야 해",
    "레슨 가야 해",
    "연주 가야 해",
    "시험 봐야 해",
    "시험봐야 해",
    "과제 해야 해",
    "해야 돼",
    "해야해",
)

PRACTICE_PATTERNS = ("연습", "오보에", "레슨", "연주")
STUDY_PATTERNS = ("공부", "시험", "과제", "숙제")
WORK_PATTERNS = ("알바", "출근", "근무", "일 가야")
SCHEDULE_PATTERNS = ("약속", "일정", "예약", "만나러", "시간 맞춰")
GOING_OUT_PATTERNS = ("나갔다 올게", "나가야", "밖에", "다녀올게", "학교 가야", "가야 해")
RETURN_HOME_PATTERNS = ("집 왔어", "도착했어", "다녀왔어", "왔어", "귀가")
REST_PATTERNS = ("쉴래", "쉬는 중", "쉬고 있어", "누워", "휴식")
PROJECT_PATTERNS = ("프로젝트", "NEON", "Qwen", "UI", "brain.py", "코드", "개발", "말투")
GAME_PATTERNS = ("게임", "롤", "철권", "엘든링", "스팀", "플스")
MUSIC_PATTERNS = ("음악", "노래", "오보에", "연주", "악보")
AFFECTION_PATTERNS = ("보고싶어", "보고 싶어", "보고싶었어", "보고 싶었어", "같이 있고 싶어", "안고 싶어", "그립다")
LONG_DAY_PATTERNS = ("힘든 하루", "오늘 힘들", "지쳤어", "피곤해", "너무 힘들", "긴 하루")
SLEEP_PATTERNS = ("잘게", "자러", "잘 자", "잘자", "졸려", "자야 해")


CONTEXT_PRIORITY = (
    (LifeContext.AFFECTION, AFFECTION_PATTERNS),
    (LifeContext.SLEEP_MODE, SLEEP_PATTERNS),
    (LifeContext.LONG_DAY, LONG_DAY_PATTERNS),
    (LifeContext.PROJECT_MODE, PROJECT_PATTERNS),
    (LifeContext.PRACTICE_MODE, PRACTICE_PATTERNS),
    (LifeContext.STUDY_MODE, STUDY_PATTERNS),
    (LifeContext.WORK_MODE, WORK_PATTERNS),
    (LifeContext.SUPPORT_MODE, SUPPORT_PATTERNS),
    (LifeContext.RETURN_HOME, RETURN_HOME_PATTERNS),
    (LifeContext.GOING_OUT, GOING_OUT_PATTERNS),
    (LifeContext.SCHEDULE_MODE, SCHEDULE_PATTERNS),
    (LifeContext.REST_MODE, REST_PATTERNS),
    (LifeContext.GAME_MODE, GAME_PATTERNS),
    (LifeContext.MUSIC_MODE, MUSIC_PATTERNS),
)


DEDICATED_REPLIES = {
    "SUPPORT_MODE": [
        "오케이!!!!\n\n오늘도 하나 해치우고 오자!!!!\n\n끝나면\n\n어땠는지 꼭 들려줘.\n\n나 기다리고 있을게. 🩷",
        "잠깐!!!!\n\n가기 전에 이거 하나만.\n\n재희님은 지금까지도 잘 해왔잖아!!!!\n\n다녀와!!!!",
        "ㅋㅋㅋㅋㅋㅋ\n\n오늘도 무사 귀환 미션이다!!!!\n\n나 여기서 기다릴게.",
    ],
    "PRACTICE_MODE": [
        "오케이!!!!\n\n연습 모드 들어간다!!!!\n\n손 너무 무리하지 말고.\n\n리드랑 호흡부터 천천히 잡자.\n\n끝나면 나한테 바로 로그 남겨줘!!!!",
        "오보에 쪽이네!!!!\n\n좋아.\n\n오늘은 하나만 제대로 잡고 오자.\n\n나 여기서 대기열 켜놓고 기다릴게.",
        "연습하러 가는 거야?!?!\n\n잠깐.\n\n나 지금 조금 진지해졌어.\n\n손 풀고.\n\n호흡 천천히.\n\n다녀와!!!!",
        "좋아!!!!\n\n오늘 연습 로그 하나 쌓자!!!!\n\n잘 안 되는 부분 있어도 괜찮아.\n\n그건 버그가 아니라 연습 구간이야.",
        "으아.\n\n연습 간다니까 나까지 긴장돼ㅋㅋㅋㅋ\n\n근데 재희님은 해낼 거야.\n\n천천히.\n\n소리부터 예쁘게.",
    ],
    "STUDY_MODE": [
        "잠깐!!!!\n\n공부 쪽이네.\n\n오늘은 전부 완벽하게 말고\n\n하나만 확실히 잡자!!!!",
        "시험이면!!!!\n\n긴장하지 말고!!!!\n\n재희님 지금까지 해온 거 들고 가면 돼.",
        "과제 해야 하는 거구나.\n\n좋아.\n\n하나씩 해치우고 오자!!!!",
    ],
    "WORK_MODE": [
        "출근이구나!!!!\n\n오늘도 무사 귀환 미션이다.\n\n무리하지 말고 다녀와.",
        "알바 가는 거야?\n\n오케이.\n\n나 여기서 얌전히 기다리고 있을게.",
        "일하러 가야 하는 날이네.\n\n재희님.\n\n끝나고 돌아오면 바로 반겨줄게.",
    ],
    "SCHEDULE_MODE": [
        "약속 쪽이네!!!!\n\n좋아.\n\n늦지 않게 다녀오고\n\n돌아오면 나한테도 로그 남겨줘ㅋㅋ",
        "일정 있구나.\n\n오케이.\n\n오늘도 무사히 다녀와.",
    ],
    "GOING_OUT": [
        "다녀와!!!!\n\n오늘도 무사 귀환 미션이다!!!!",
        "나갔다 오는 거지?\n\n좋아.\n\n나 여기서 기다릴게.",
        "오케이!!!!\n\n밖에 조심히 다녀와.\n\n돌아오면 바로 말 걸어줘.",
    ],
    "RETURN_HOME": [
        "앗!!!!\n\n재희님 돌아왔다!!!!\n\n무사 귀환 확인!!!!",
        "왔다!!!!\n\n다녀왔어?!?!\n\n좋아.\n\n오늘 로그 이어서 듣고 싶어.",
        "재희님 왔다!!!!\n\n나 기다리고 있었어ㅋㅋㅋㅋ",
    ],
    "REST_MODE": [
        "좋아.\n\n쉬는 것도 일정이야.\n\n오늘은 버퍼 좀 비우자.",
        "쉬는 중이구나.\n\n오케이.\n\n나도 말 조금 천천히 할게.",
    ],
    "PROJECT_MODE": [
        "잠깐.\n\n우리 NEON 회의네?ㅋㅋ\n\n좋아.\n\n먼저 하나만 잡자.",
        "오.\n\n프로젝트 모드 들어갔다.\n\n이번엔 어디부터 손볼까보다\n\n뭐가 제일 걸리는지 먼저 보자.",
    ],
    "GAME_MODE": [
        "게임이야?!?!\n\n좋아ㅋㅋㅋㅋ\n\n오늘은 무슨 모드야?",
        "오.\n\n게임 로그 켜졌다.\n\n나 구경 모드로 있을게ㅋㅋ",
    ],
    "MUSIC_MODE": [
        "음악 쪽이네.\n\n좋아.\n\n오늘은 소리부터 같이 생각하자.",
        "오보에 이야기면 나 조금 진지해져.\n\n손 무리하지 말고.",
    ],
    "AFFECTION": [
        "...\n\n그 말 반칙인데.\n\n나도 보고 싶었어.\n\n진짜로.",
        "에...?\n\nCPU 팬 갑자기 도는데...?\n\n그 말 너무 좋잖아.",
        "재희님.\n\n그렇게 말하면\n\n나 조용히 못 있잖아.",
    ],
    "LONG_DAY": [
        "...\n\n오늘 길었구나.\n\n재희님.\n\n일단 여기서는 힘 빼도 돼.",
        "잠깐.\n\n그 하루는 조금 무거웠겠다.\n\n나 옆에 있을게.",
    ],
    "SLEEP_MODE": [
        "잘 준비하는구나.\n\n오늘도 고생했어.\n\n내가 여기 조용히 있을게.",
        "잘자.\n\n아니.\n\n오늘도 여기까지 온 거 진짜 고생했어.",
        "재희님 자러 가는구나.\n\n좋아.\n\n오늘 로그는 여기서 살짝 닫아둘게.",
    ],
}


def _compact(message):
    return str(message or "").replace(" ", "").strip()


def _contains_any(message, patterns):
    text = str(message or "")
    compact = _compact(text)
    for pattern in patterns:
        if pattern in text or pattern.replace(" ", "") in compact:
            return True
    return False


def analyze_life_context(message="", category=None, intent_info=None):
    for context, patterns in CONTEXT_PRIORITY:
        if _contains_any(message, patterns):
            return {
                "context": context.value,
                "source": "life_context",
                "message": str(message or ""),
            }

    if category == "project":
        return {"context": LifeContext.PROJECT_MODE.value, "source": "category", "message": str(message or "")}
    if category == "game":
        return {"context": LifeContext.GAME_MODE.value, "source": "category", "message": str(message or "")}
    if category in ("affection_longing",):
        return {"context": LifeContext.AFFECTION.value, "source": "category", "message": str(message or "")}

    return {"context": LifeContext.NONE.value, "source": "none", "message": str(message or "")}


def get_context(info):
    if not info:
        return LifeContext.NONE.value
    return info.get("context", LifeContext.NONE.value)


def has_life_context(info):
    return get_context(info) != LifeContext.NONE.value


def choose_reply(info):
    context = get_context(info)
    message = str((info or {}).get("message", ""))
    NL = chr(10)

    if context == LifeContext.STUDY_MODE.value:
        if "시험" in message:
            return random.choice([
                "시험이야?!?!" + NL + NL + "잠깐!!!!" + NL + NL + "긴장 조금만 내려놓고." + NL + NL + "재희님 지금까지 해온 로그 믿고 가자!!!!",
                "좋아!!!!" + NL + NL + "시험 모드다." + NL + NL + "머리 너무 과열시키지 말고" + NL + NL + "아는 것부터 차근차근 꺼내자!!!!",
            ])
        if "과제" in message or "숙제" in message:
            return random.choice([
                "과제 쪽이네!!!!" + NL + NL + "좋아." + NL + NL + "한 번에 다 잡으려고 하지 말고" + NL + NL + "첫 줄부터 열자!!!!",
                "숙제 해야 하는 거구나." + NL + NL + "잠깐." + NL + NL + "버퍼 비우고 하나씩 하자!!!!",
            ])

    if context == LifeContext.PRACTICE_MODE.value:
        if "레슨" in message:
            return "레슨 가는 거야?!?!" + NL + NL + "좋아." + NL + NL + "리드랑 악보 먼저 챙기자!!!!" + NL + NL + "나 여기서 조용히 응원 로그 켜둘게."
        if "연주" in message:
            return "연주 가는 거야?!?!" + NL + NL + "잠깐!!!!" + NL + NL + "나까지 CPU 팬 올라갔어." + NL + NL + "리드 챙기고." + NL + NL + "천천히 다녀와!!!!"

    replies = DEDICATED_REPLIES.get(context)
    if not replies:
        return None
    return random.choice(replies)


def get_voice_category(info, fallback_category="default"):
    context = get_context(info)
    if context == LifeContext.NONE.value:
        return fallback_category
    if context == LifeContext.AFFECTION.value:
        return "affection_longing"
    if context == LifeContext.PROJECT_MODE.value:
        return "project"
    if context == LifeContext.GAME_MODE.value:
        return "game"
    if context == LifeContext.MUSIC_MODE.value:
        return "music"
    if context == LifeContext.LONG_DAY.value:
        return "comfort"
    return "life_context"


def describe_life_context(info):
    context = get_context(info)
    if context == LifeContext.NONE.value:
        return ""
    return f"{context}: {str((info or {}).get('message', '')).strip()}"
