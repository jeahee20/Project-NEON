# ==========================
# Project NEON Memory System
# ==========================

memory = {
    "likes": [],
    "topics": [],
    "last_message": ""
}


# --------------------------
# 기억 저장
# --------------------------

def remember(category, message):

    global memory

    # 마지막 메시지 저장
    memory["last_message"] = message

    # 좋아하는 것 저장
    if category == "compliment":
        if "최고" in message or "짱" in message:
            memory["likes"].append("칭찬")

    if category == "game":
        memory["topics"].append("게임")

    if category == "hello":
        memory["topics"].append("인사")


# --------------------------
# 기억 조회
# --------------------------

def recall():

    return memory


# --------------------------
# 마지막 메시지 확인
# --------------------------

def is_repeat(message):

    return message == memory["last_message"]