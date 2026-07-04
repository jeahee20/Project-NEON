import time


ONLINE = "ONLINE"
IDLE = "IDLE"
BUSY = "BUSY"
SLEEPING = "SLEEPING"

CHATTING = "CHATTING"
GAME = "GAME"
WORK = "WORK"
PRACTICE = "PRACTICE"
REST = "REST"
EATING = "EATING"
OUTSIDE = "OUTSIDE"

IDLE_SECONDS = 20 * 60
BUSY_AUTO_TALK_SECONDS = 40 * 60
AUTO_TALK_COOLDOWN_SECONDS = 20 * 60

current_status = ONLINE
current_activity = CHATTING
last_message_time = time.time()
last_auto_talk_time = 0
logs = []


def add_log(event):
    logs.append({
        "time": time.strftime("%H:%M"),
        "event": event,
        "status": current_status,
        "activity": current_activity,
    })

    del logs[:-100]


def set_status(status):
    global current_status

    if status not in (ONLINE, IDLE, BUSY, SLEEPING):
        return current_status

    current_status = status
    add_log(f"status:{status}")
    return current_status


def get_status():
    global current_status

    if (
        current_status != SLEEPING
        and current_status != BUSY
        and time.time() - last_message_time >= IDLE_SECONDS
    ):
        current_status = IDLE

    return current_status


def update_activity(message):
    global current_activity

    message = str(message).lower().strip()

    if "게임" in message:
        current_activity = GAME
    elif (
        "작업" in message
        or "코딩" in message
    ):
        current_activity = WORK
    elif (
        "오보에" in message
        or "연습" in message
    ):
        current_activity = PRACTICE
    elif (
        "쉴게" in message
        or "쉬는 중" in message
        or "휴식" in message
    ):
        current_activity = REST
    elif "밥" in message:
        current_activity = EATING
    elif "나갔다 올게" in message:
        current_activity = OUTSIDE
    else:
        current_activity = CHATTING

    add_log(f"activity:{current_activity}")
    return current_activity


def update_presence(message):
    global last_message_time

    message = str(message).lower().strip()
    last_message_time = time.time()

    if "잘게" in message:
        set_status(SLEEPING)
    elif (
        "작업" in message
        or "코딩" in message
        or "게임" in message
        or "오보에" in message
        or "연습" in message
    ):
        set_status(BUSY)
    else:
        set_status(ONLINE)

    update_activity(message)
    return {
        "status": current_status,
        "activity": current_activity,
        "last_message_time": last_message_time,
    }


def get_activity():
    return current_activity


def get_logs():
    return list(logs)


def should_start_conversation():
    global current_status

    now = time.time()
    idle_time = now - last_message_time
    auto_talk_gap = now - last_auto_talk_time

    if current_status == SLEEPING:
        return False

    if auto_talk_gap < AUTO_TALK_COOLDOWN_SECONDS:
        return False

    if current_status == BUSY:
        return idle_time >= BUSY_AUTO_TALK_SECONDS

    if idle_time >= IDLE_SECONDS:
        current_status = IDLE
        return True

    return False


def mark_auto_talk():
    global last_auto_talk_time

    last_auto_talk_time = time.time()
    add_log("auto_talk")
    return last_auto_talk_time


def get_presence_talk_key():
    status = get_status()

    if status == SLEEPING:
        return SLEEPING

    if status == IDLE:
        return IDLE

    if current_activity in (
        GAME,
        WORK,
        PRACTICE,
        REST,
    ):
        return current_activity

    return status
