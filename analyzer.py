# ==========================
# Project NEON Analyzer
# ==========================

def analyze(message):

    message = message.lower().strip()

    if "안녕" in message:
        return "hello"

    if "ㅋㅋ" in message or "ㅎㅎ" in message:
        return "laugh"

    if "게임" in message:
        return "game"

    if "고마워" in message or "감사" in message:
        return "thanks"

    if (
        "잘한다" in message
        or "최고" in message
        or "귀엽" in message
        or "멋지" in message
    ):
        return "compliment"

    return "default"