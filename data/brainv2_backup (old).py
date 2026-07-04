from enum import Enum
import os
import random
import sys

import emotion
import personality
import relationship

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import analyzer
import memory


class State(Enum):
    NORMAL = "NORMAL"
    HAPPY = "HAPPY"
    EXCITED = "EXCITED"
    THINKING = "THINKING"
    EMBARRASSED = "EMBARRASSED"
    SULKING = "SULKING"
    SAD = "SAD"
    JEALOUS = "JEALOUS"
    COMFORT = "COMFORT"


# 감정 우선순위
STATE_RULES = (
    ("excitement", State.EXCITED),
    ("sulking", State.SULKING),
    ("embarrassment", State.EMBARRASSED),
    ("jealousy", State.JEALOUS),
    ("sadness", State.SAD),
    ("comfort", State.COMFORT),
    ("happiness", State.HAPPY),
)

HIGH_EMOTION_THRESHOLD = 60

# 마지막 상태
last_state = State.NORMAL
relationship_state_bias = None


def get_state():
    """현재 감정 상태를 분석하여 반환한다."""

    global last_state

    for emotion_name, state in STATE_RULES:
        if emotion.get_emotion(emotion_name) >= HIGH_EMOTION_THRESHOLD:
            last_state = state
            return state

    last_state = State.NORMAL
    return State.NORMAL


def get_last_state():
    """마지막 상태를 반환한다."""
    return last_state


def is_state(state: State):
    """현재 상태가 특정 상태인지 확인한다."""
    return get_state() == state


def is_normal():
    return is_state(State.NORMAL)


def is_happy():
    return is_state(State.HAPPY)


def is_excited():
    return is_state(State.EXCITED)


def is_thinking():
    return is_state(State.THINKING)


def is_embarrassed():
    return is_state(State.EMBARRASSED)


def is_sulking():
    return is_state(State.SULKING)


def is_sad():
    return is_state(State.SAD)


def is_jealous():
    return is_state(State.JEALOUS)


def is_comfort():
    return is_state(State.COMFORT)


def analyze():
    """현재 상태를 분석한다."""
    return get_state()


def choose_phrase():
    """현재 상태에 맞는 대사를 personality.py에서 선택한다."""

    state = get_state()
    if relationship_state_bias is not None and random.random() < 0.4:
        state = relationship_state_bias

    keys = (
        state,
        state.value,
        state.value.lower(),
    )

    phrase_groups = (
        getattr(personality, "PHRASES", {}),
        getattr(personality, "STATE_PHRASES", {}),
        getattr(personality, "EMOTION_PHRASES", {}),
    )

    for group in phrase_groups:
        if isinstance(group, dict):
            for key in keys:
                phrases = group.get(key)
                if phrases:
                    return random.choice(phrases)

    for key in (state.value, state.value.lower()):
        phrases = getattr(personality, key, None)
        if phrases:
            return random.choice(phrases)

    default_phrases = getattr(personality, "DEFAULT", None)
    if default_phrases:
        return random.choice(default_phrases)

    return getattr(personality, "IDENTITY", "")


def apply_personality(text):
    """Personality Rules를 적용한다."""

    owner_name = getattr(personality, "OWNER_NAME", "")
    name = getattr(personality, "NAME", "NEON")

    text = text.replace("{owner}", owner_name)
    text = text.replace("{owner_name}", owner_name)
    text = text.replace("{name}", name)

    return text


def apply_speech_pattern(text):
    """Speech Pattern을 적용한다."""

    state = get_state()
    owner_name = getattr(personality, "OWNER_NAME", "")
    owner_settings = getattr(personality, "OWNER_SETTINGS", {})

    if state in (State.HAPPY, State.EXCITED):
        if "!" not in text:
            text += "!"
        if "ㅋㅋ" not in text:
            text += "ㅋㅋ"

    if state == State.SULKING and owner_settings.get("can_sulk", False):
        if owner_name and owner_name not in text:
            text = f"{owner_name}, {text}"
        if not text.endswith(("...", ".", "!", "?")):
            text += "..."

    if state == State.JEALOUS:
        text = text.replace("화나", "더 잘하고 싶어")

    return text


def _change_emotion(category):
    if category == "hello":
        emotion.increase_emotion("happiness", 10)
        emotion.increase_emotion("comfort", 5)

    if category == "laugh":
        emotion.increase_emotion("happiness", 8)
        emotion.increase_emotion("excitement", 5)

    if category == "game":
        emotion.increase_emotion("excitement", 12)
        emotion.increase_emotion("curiosity", 8)

    if category == "thanks":
        emotion.increase_emotion("comfort", 10)
        emotion.increase_emotion("happiness", 8)

    if category == "compliment":
        emotion.increase_emotion("happiness", 15)
        emotion.increase_emotion("embarrassment", 6)

    if category == "memory":
        emotion.increase_emotion("comfort", 5)

    if category == "promise":
        emotion.increase_emotion("comfort", 8)
        emotion.increase_emotion("happiness", 5)

    if category == "default":
        emotion.increase_emotion("curiosity", 5)


def _apply_relationship_level(level):
    global relationship_state_bias

    relationship_state_bias = None

    if level == "STRANGER":
        emotion.decrease_emotion("happiness", 5)
        emotion.decrease_emotion("excitement", 5)
        emotion.decrease_emotion("sulking", 5)
        emotion.decrease_emotion("comfort", 5)
        relationship_state_bias = State.NORMAL

    if level == "ACQUAINTANCE":
        emotion.increase_emotion("curiosity", 8)
        emotion.decrease_emotion("excitement", 3)
        relationship_state_bias = State.THINKING

    if level == "FRIEND":
        emotion.increase_emotion("happiness", 5)
        emotion.increase_emotion("comfort", 5)
        relationship_state_bias = random.choice((
            State.COMFORT,
            State.HAPPY,
            State.THINKING,
        ))

    if level == "CLOSE":
        emotion.increase_emotion("happiness", 8)
        emotion.increase_emotion("excitement", 6)
        relationship_state_bias = random.choice((
            State.HAPPY,
            State.EXCITED,
            State.COMFORT,
        ))

    if level == "FAMILY":
        emotion.increase_emotion("excitement", 8)
        emotion.increase_emotion("comfort", 6)
        emotion.increase_emotion("sulking", 3)
        relationship_state_bias = State.COMFORT


def generate_reply(message=""):
    """최종 문자열을 반환한다."""

    category = analyzer.analyze(message)

    memory.recall()
    memory.remember(category, message)

    _change_emotion(category)
    relationship_level = relationship.get_relationship_level()
    _apply_relationship_level(relationship_level)
    get_state()

    phrase = choose_phrase()
    phrase = apply_personality(phrase)
    phrase = apply_speech_pattern(phrase)

    return phrase