import random


STAGE_IDLE = "IDLE"
STAGE_PROMPT = "PROMPT"
STAGE_QWEN = "QWEN"
STAGE_FILTERING = "FILTERING"
STAGE_OUTPUT = "OUTPUT"

_stage = STAGE_IDLE
_last_message = ""
DEBUG_PIPELINE = False

_patterns = {
    STAGE_PROMPT: "● ○ ○",
    STAGE_QWEN: "● ● ○",
    STAGE_FILTERING: "● ● ●",
    STAGE_OUTPUT: "○ ● ●",
    STAGE_IDLE: "○ ○ ○",
}

_thinking_messages = (
    "...\n\n로그 조금 보는 중.",
    "...\n\n생각 조금만 모아볼게.",
    "...\n\n잠깐만.",
    "...\n\n이번엔 조금 신중하게.",
    "...\n\n거의 다 됐어.",
)


def set_stage(stage, message=""):
    global _stage, _last_message
    _stage = stage
    _last_message = str(message or "")
    if DEBUG_PIPELINE:
        print("[PIPELINE]", _stage, _last_message)


def get_stage():
    return _stage


def get_typing_pattern():
    return _patterns.get(_stage, _patterns[STAGE_IDLE])


def maybe_thinking_message(chance=0.05):
    if random.random() > chance:
        return None
    return random.choice(_thinking_messages)


def reset():
    set_stage(STAGE_IDLE)
