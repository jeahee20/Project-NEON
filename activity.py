import time


last_user_message_time = time.time()
current_activity = "idle"

AUTO_TALK_IDLE_SECONDS = 20


def update_activity(message):
    global last_user_message_time
    global current_activity

    message = str(message).lower().strip()
    last_user_message_time = time.time()

    if message == "":
        current_activity = "waiting"
        return current_activity

    if message == "typing":
        current_activity = "typing"
        return current_activity

    if (
        "게임" in message
        or "롤" in message
        or "철권" in message
        or "플스" in message
        or "스팀" in message
    ):
        current_activity = "game"
        return current_activity

    if (
        "작업" in message
        or "코딩" in message
        or "연습" in message
    ):
        current_activity = "work"
        return current_activity

    if (
        "잘게" in message
        or "잘 자" in message
        or "잘자" in message
    ):
        current_activity = "sleep"
        return current_activity

    if "밥" in message:
        current_activity = "meal"
        return current_activity

    if "나갔다 올게" in message:
        current_activity = "away"
        return current_activity

    current_activity = "chatting"
    return current_activity


def get_activity():
    return current_activity


def should_auto_talk():
    return time.time() - last_user_message_time >= AUTO_TALK_IDLE_SECONDS


def get_activity_status():
    if current_activity == "typing":
        return "입력 중"

    if current_activity == "game":
        return "게임 지켜보는 중"

    if current_activity == "work":
        return "작업 지켜보는 중"

    if current_activity == "sleep":
        return "잘 자라고 기다리는 중"

    if current_activity == "meal":
        return "밥 먹는 거 기다리는 중"

    if current_activity == "away":
        return "재희님 기다리는 중"

    if current_activity == "waiting":
        return "아무 말 없이 대기 중"

    if should_auto_talk():
        return "재희님 기다리는 중"

    if current_activity == "chatting":
        return "대화 중"

    return "ONLINE"
