# ==========================
# Project NEON Memory System
# ==========================

import json
import random


memory = {
    "profile": {},
    "likes": [],
    "dislikes": [],
    "topics": [],
    "memories": [],
    "promises": [],
    "last_message": ""
}

MEMORY_FILE = "memory.json"


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
            if "칭찬" not in memory["likes"]:
                memory["likes"].append("칭찬")

    if category == "game":
        if "게임" not in memory["topics"]:
            memory["topics"].append("게임")

    if category == "hello":
        if "인사" not in memory["topics"]:
            memory["topics"].append("인사")

    if category == "memory":
        memory["memories"].append(message)

    if category == "promise":
        memory["promises"].append(message)

    save_memory()


# --------------------------
# 기억 조회
# --------------------------

def recall():

    return memory


def recall_random(category=None):

    if category is None:
        memories = memory["memories"]
    else:
        memories = memory.get(category, [])

    if not memories:
        return None

    return random.choice(memories)


# --------------------------
# 마지막 메시지 확인
# --------------------------

def is_repeat(message):

    return message == memory["last_message"]


# --------------------------
# 기억 저장 파일
# --------------------------

def save_memory(file_path=MEMORY_FILE):

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(memory, file, ensure_ascii=False, indent=4)


# --------------------------
# 기억 불러오기
# --------------------------

def load_memory(file_path=MEMORY_FILE):

    global memory

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            loaded_memory = json.load(file)
    except FileNotFoundError:
        return memory

    memory.update(loaded_memory)
    return memory