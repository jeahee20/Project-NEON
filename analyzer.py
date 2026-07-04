# ==========================
# Project NEON Analyzer
# ==========================

from datetime import datetime

import typing_dna


def _time_hello_category():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        return "morning_hello"
    if 12 <= hour < 18:
        return "afternoon_hello"
    if 18 <= hour < 24:
        return "night_hello"
    return "dawn_hello"


def normalize_message(message):
    typo_map = {
        "안뇽ㅎ": "안녕",
        "안녀": "안녕",
        "안뇽": "안녕",
        "안냥": "안녕",
        "뭐하냐": "뭐해",
        "뭐햐": "뭐해",
        "뭐하": "뭐해",
        "모해": "뭐해",
        "머해": "뭐해",
        "ㅇㅇㅎ": "웅",
        "그래ㅎ": "웅",
        "구래ㅎ": "웅",
        "어ㅎ": "웅",
        "아ㅎ": "웅",
        "웅ㅎ": "웅",
        "웅웅": "웅",
        "응응": "웅",
        "응ㅎ": "웅",
        "엉ㅎ": "웅",
        "엉": "웅",
        "ㅇㅇ": "웅",
        "넵ㅎ": "웅",
        "넵": "웅",
        "넹": "웅",
        "고마워어": "고마워",
        "고마어": "고마워",
        "감사해": "고마워",
        "ㄱㅅ": "고마워",
        "좋아해ㅐ": "좋아해",
        "좋아햐": "좋아해",
        "조아해": "좋아해",
        "좋아ㅏ": "좋아",
        "조아": "좋아",
        "사랑해ㅐ": "사랑해",
        "사랑행": "사랑해",
        "힘드러ㅜ": "힘들어",
        "힘들어ㅠ": "힘들어",
        "힘드러": "힘들어",
        "힘들다": "힘들어",
        "기여워": "귀여워",
        "귀여어": "귀여워",
        "귀엽다": "귀여워",
        "뭐야?": "뭐야",
        "머야": "뭐야",
        "모야": "뭐야",
        "왜애": "왜",
        "웨": "왜",
        "잘자ㅏ": "잘자",
        "잘쟈": "잘자",
    }

    for typo, fixed in typo_map.items():
        if typo in message:
            message = message.replace(typo, fixed)

    exact_typo_map = {
        "외": "왜",
        "네": "웅",
        "네ㅎ": "웅",
    }

    return exact_typo_map.get(message, message)


def analyze(message):

    message = typing_dna.normalize_for_analysis(str(message).lower().strip())
    original_message = message

    if typing_dna.analyze(message).get("affection_priority"):
        return "affection_longing"

    if original_message in (
        "웅ㅎ",
        "웅ㅎㅎ",
        "웅ㅋㅋ",
        "응ㅎ",
        "응ㅎㅎ",
        "응ㅋㅋ",
        "어ㅎ",
        "어ㅎㅎ",
        "아ㅎ",
        "아ㅎㅎ",
        "그래ㅎ",
        "그래ㅎㅎ",
        "네ㅎ",
        "네ㅎㅎ",
        "넹",
        "넹ㅎ",
        "넹ㅎㅎ",
    ):
        return "soft_ack"

    message = normalize_message(message)

    compact_message = message.replace(" ", "")

    conversation_words = (
        "\ubb50\ud574",
        "\ubaa8\ud574",
        "\uba38\ud574",
        "\ubb50\ud568",
        "\ubb50\ud558\uace0\uc788\uc5b4",
        "\ubb50\ud558\uace0\uc788\uc5c8\uc5b4",
        "\ubb50\ud558\ub294\uc911",
        "\ubb50\ud558\uad6c\uc788\uc5b4",
        "\uc9c0\uae08\ubb50\ud574",
    )

    if any(word in compact_message for word in conversation_words):
        return "conversation_status"

    if message == "auto_talk":
        return "auto_talk"

    compact_message = message.replace(" ", "")
    if any(word in compact_message for word in (
        "\ubcf4\uace0\uc2f6\uc5b4",
        "\ubcf4\uace0\uc2f6\uc5c8\uc5b4",
        "\ubcf4\uace0\uc2f6\ub2e4",
    )):
        return "affection_longing"

    compliment_priority_words = (
        "\uc88b\uc544\ud574",
        "\uc0ac\ub791\ud574",
        "\ucd5c\uace0",
        "\ucd5c\uace0\uc57c",
        "\uadc0\uc5ec\uc6cc",
        "\uae30\uc5ec\uc6cc",
        "\uc798\ud588\uc5b4",
        "\ub300\ub2e8\ud574",
        "\uba4b\uc838",
        "\uc608\ubed0",
        "\ucc9c\uc7ac",
        "\uc0ac\ub791\uc2a4\ub7ec\uc6cc",
        "\uae30\ud2b9\ud574",
    )

    if any(word in message for word in compliment_priority_words):
        return "compliment"

    approve_words = (
        "\uc88b\uc544",
        "\uc624\ucf00\uc774",
        "\uc624\ucf00",
        "\uc6c5",
        "\u3147\u314b",
        "\uadf8\ub798",
        "\ub9c8\uc74c\uc5d0 \ub4e4\uc5b4",
        "\ub9d8\uc5d0 \ub4e4\uc5b4",
        "\uc88b\ub2e4",
        "\ud1b5\uacfc",
        "\ud569\uaca9",
        "\ucc44\ud0dd",
        "\uc774\ub300\ub85c",
        "\uc774\uac70\uc57c",
    )

    if any(word in message for word in approve_words):
        return "approve"

    project_words = (
        "\ud504\ub85c\uc81d\ud2b8",
        "project",
        "neon",
        "qwen",
        "brain.py",
        "\ube0c\ub808\uc778",
        "\ucf54\ub4dc",
        "\uc124\uacc4",
        "\ubc29\ud5a5",
        "\uace0\ubbfc",
        "\ub9ac\ud329\ud1a0\ub9c1",
        "\uba54\ubaa8\ub9ac",
        "\uac10\uc815",
        "emotion",
        "memory",
        "presence",
        "\uc120\ud1a1",
        "\uc790\ub3d9\ub300\ud654",
        "ui",
        "\ub514\uc790\uc778",
        "\ub9d0\ud22c",
        "\ud504\ub86c\ud504\ud2b8",
        "\ub370\uc774\ud130\uc14b",
        "dialogue",
        "typing",
        "\ud0c0\uc774\ud551",
        "old",
        "\ud3f4\ub354",
        "discord",
    )

    if any(word in message for word in project_words):
        return "project"

    if message in (
        "응",
        "웅",
        "엉",
        "어",
        "ㅇㅇ",
        "그래",
        "구래",
        "어ㅎ",
        "아ㅎ",
        "웅ㅎ",
        "응ㅎ",
        "엉ㅎ",
        "그래ㅎ",
        "구래ㅎ",
        "ㅇㅇㅎ",
        "넹",
        "네",
        "네ㅎ",
        "넵",
        "넵ㅎ",
        "웅웅",
        "응응",
    ):
        return "ack"

    if (
        "뭐해" in message
        or "모해" in message
        or "뭐 하고 있어" in message
        or "뭐하는 중" in message
        or "지금 뭐해" in message
        or "뭐하냐" in message
        or "뭐하구 있어" in message
        or "뭐하구있어" in message
    ):
        return "daily"

    if message in (
        "어?",
        "왜?",
        "뭐?",
        "뭐야",
        "그게 무슨",
        "그래ㅎㅎ",
        "음",
        "흠",
    ):
        return "default"

    if (
        "안녕" in message
        or "안녀" in message
        or "하이" in message
        or "ㅎㅇ" in message
        or "왔어" in message
        or "나 왔어" in message
        or "다녀왔어" in message
        or "좋은 아침" in message
        or "좋은밤" in message
        or "잘잤어" in message
        or "헬로" in message
    ):
        return _time_hello_category()

    if (
        "ㅋㅋ" in message
        or "ㅎㅎ" in message
        or "웃겨" in message
        or "웃기네" in message
        or "웃기다" in message
        or "푸하하" in message
        or "하하" in message
    ):
        return "laugh"

    if (
        "고마워" in message
        or "감사" in message
        or "땡큐" in message
        or "고맙다" in message
        or "고맙습니다" in message
    ):
        return "thanks"

    if (
        "최고" in message
        or "최고야" in message
        or "귀여워" in message
        or "잘했어" in message
        or "대단해" in message
        or "멋져" in message
        or "좋아해" in message
        or "사랑해" in message
        or "사랑스러워" in message
        or "사랑스럽다" in message
        or "천재" in message
        or "예뻐" in message
        or "자랑스러워" in message
    ):
        return "compliment"

    comfort_negative = (
        "안 힘들어",
        "안힘들어",
        "안 힘든",
        "안힘든",
        "안 아파",
        "안아파",
        "안 슬퍼",
        "안슬퍼",
        "안 우울해",
        "안우울해",
        "힘든 건 아니야",
        "힘든건 아니야",
        "슬픈 건 아니야",
        "슬픈건 아니야",
        "괜찮아",
        "괜찮은데",
    )

    comfort_words = (
        "힘들어",
        "지쳤어",
        "슬퍼",
        "우울해",
        "우울",
        "속상해",
        "속상",
        "지쳤",
        "아파",
        "불안해",
        "불안",
        "무서워",
        "무서워",
        "외로워",
        "망했어",
        "하기 싫어",
    )

    if any(word in message for word in comfort_words):
        if not any(word in message for word in comfort_negative):
            return "comfort"

    if (
        "게임" in message
        or "롤" in message
        or "철권" in message
        or "스트리트파이터" in message
        or "엘든링" in message
        or "플스" in message
        or "스팀" in message
    ):
        return "game"

    if (
        "기억해" in message
        or "저장해" in message
        or "기억해줘" in message
        or "저장해줘" in message
        or "잊지마" in message
    ):
        return "memory"

    if (
        "약속" in message
        or "내일" in message
        or "나중에" in message
        or "같이 하자" in message
        or "같이 하자!" in message
        or "다음에 하자" in message
        or "다음에" in message
    ):
        return "promise"

    return "default"
