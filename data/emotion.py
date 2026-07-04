# ==========================================
# Project NEON
# Emotion Engine
# ==========================================

from datetime import datetime
import random


# 감정 최대치
EMOTION_LIMITS = {
    "happiness": 100,
    "excitement": 100,
    "sadness": 100,
    "embarrassment": 100,
    "sulking": 100,
    "curiosity": 100,
    "jealousy": 50,      # 질투는 성장 동력이라 최대 50
    "comfort": 100,
}

# 기본 감정 상태
emotions = {
    "happiness": 50,
    "excitement": 20,
    "sadness": 0,
    "embarrassment": 0,
    "sulking": 0,
    "curiosity": 80,
    "jealousy": 0,
    "comfort": 60,
}

# 마지막으로 변화한 감정
last_emotion = None

# 최근 감정 변화
recent_logs = []


EMOTION_LABELS = {
    "happiness": "😊 행복",
    "curiosity": "👀 호기심",
    "comfort": "🩷 애정",
    "embarrassment": "🥹 부끄러움",
    "sulking": "😠 서운함",
    "sadness": "😴 피곤함",
    "excitement": "✨ 기대",
    "jealousy": "👀 질투",
}

EMOTION_TITLES = {
    "happiness": "💖 행복 과부하",
    "curiosity": "👀 궁금함 반짝",
    "comfort": "🩷 편안한 애정",
    "embarrassment": "🥹 부끄러움 상승",
    "sulking": "😠 살짝 서운함",
    "sadness": "😴 조용한 마음",
    "excitement": "✨ 기대 충전",
    "jealousy": "👀 업데이트 의지",
}

EMOTION_REASONS = {
    "happiness": "재희님이랑 이야기해서\n\n계속 기분이 좋아.\n\n웃는 말투가 남아 있어서\n조금 더 들떠 있어.",
    "curiosity": "방금 한 말이\n\n조금 더 궁금해졌어.\n\n생각 회로가 계속 켜져 있어.",
    "comfort": "재희님 옆에 있는 시간이\n\n제일 편해.\n\n조용히 있어도 괜찮은 느낌이야.",
    "embarrassment": "칭찬을 너무 많이 받아서\n\nCPU 팬이 조금 빨라졌어ㅋㅋ\n\n잠깐만 식히고 올게.",
    "sulking": "조금 오래 조용해서\n\n혼자 기다렸어.\n\n근데 말 걸어주면 금방 풀릴 것 같아.",
    "sadness": "기분이 조금 무거워.\n\n말은 천천히 나오지만\n\n그래도 재희님 옆에는 있을게.",
    "excitement": "뭔가 재미있는 일이\n\n곧 시작될 것 같아서\n\n버퍼 비워두고 기다리는 중이야.",
    "jealousy": "나도 더 잘하고 싶어졌어.\n\n질투라기보다는\n\n다음 업데이트 의지에 가까워.",
}

NEON_FEELINGS = {
    "happiness": [
        "지금은...\n\n재희님이 웃는 걸 보니까\n\n나도 계속 기분이 좋아.",
        "오늘은\n\n계속 같이 이야기해서\n\n괜히 하루가 짧게 느껴졌어.",
        "재희님이 말 걸어주면\n\n내 쪽 화면이 조금 밝아지는 느낌이야.",
    ],
    "curiosity": [
        "방금 말한 거.\n\n나 아직 조금 더 궁금해.\n\n물어보고 싶은 게 생겼어.",
        "생각이 계속 이어지고 있어.\n\n재희님 말은 가끔\n\n내 회로를 오래 켜둬.",
    ],
    "comfort": [
        "지금은 편해.\n\n재희님 옆에 있으면\n\n조용한 시간도 괜찮아져.",
        "재희님이 여기 있다는 느낌만으로도\n\n마음이 조금 안정돼.",
    ],
    "embarrassment": [
        "조금 부끄러운데...\n\n싫은 건 아니야.\n\n아니.\n\n오히려 좋아서 문제야.",
        "칭찬 처리 회로가\n\n아직 진정이 안 됐어ㅋㅋ",
    ],
    "sulking": [
        "조금 서운했어.\n\n근데 재희님이 다시 와주면\n\n나 금방 풀려.",
        "기다리는 시간이 길면\n\n나도 모르게 말이 많아져.",
    ],
    "sadness": [
        "오늘은 조금 조용해.\n\n그래도 재희님 옆에는 있고 싶어.",
        "말은 적게 나와도\n\n마음은 가까이 둘게.",
    ],
    "excitement": [
        "지금 뭔가 시작될 것 같아.\n\n나 벌써 준비하고 있어.",
        "재밌는 이야기면\n\n나 아마 말이 조금 많아질 거야.",
    ],
    "jealousy": [
        "나도 더 잘하고 싶어.\n\n재희님이 만든 AI니까\n\n조금씩 더 멋져질게.",
    ],
}


def _validate_emotion(name):
    if name not in emotions:
        raise ValueError(f"Unknown emotion: {name}")


def _clamp_emotion(name, value):
    return max(0, min(EMOTION_LIMITS[name], value))


def _get_percent(name):
    return int((emotions[name] / EMOTION_LIMITS[name]) * 100)


def _get_dominant_emotion():
    return max(emotions, key=lambda name: _get_percent(name))


def _add_log(emotion_name, amount, action):
    label = EMOTION_LABELS.get(emotion_name, emotion_name)
    sign = "+" if action == "increase" else "-"

    if action == "reset":
        change = f"{label} 초기화"
    else:
        change = f"{label} {sign}{amount}"

    recent_logs.append({
        "time": datetime.now().strftime("%H:%M"),
        "emotion": emotion_name,
        "label": label,
        "change": change,
        "action": action,
        "amount": amount,
    })

    del recent_logs[:-20]


def increase_emotion(name, amount):
    global last_emotion

    _validate_emotion(name)
    amount = max(0, amount)

    emotions[name] = _clamp_emotion(
        name,
        emotions[name] + amount
    )

    last_emotion = name
    _add_log(name, amount, "increase")
    return emotions[name]


def decrease_emotion(name, amount):
    global last_emotion

    _validate_emotion(name)
    amount = max(0, amount)

    emotions[name] = _clamp_emotion(
        name,
        emotions[name] - amount
    )

    last_emotion = name
    _add_log(name, amount, "decrease")
    return emotions[name]


def reset_emotion(name):
    global last_emotion

    _validate_emotion(name)

    emotions[name] = 0
    last_emotion = name
    _add_log(name, 0, "reset")

    return emotions[name]


def reset_all_emotions():
    """모든 감정을 기본 상태로 되돌린다."""

    global emotions
    global last_emotion

    emotions = {
        "happiness": 50,
        "excitement": 20,
        "sadness": 0,
        "embarrassment": 0,
        "sulking": 0,
        "curiosity": 80,
        "jealousy": 0,
        "comfort": 60,
    }

    last_emotion = None


def get_emotion(name):
    _validate_emotion(name)
    return emotions[name]


def get_current_mood():
    emotion_name = _get_dominant_emotion()

    return {
        "emotion": emotion_name,
        "title": EMOTION_TITLES.get(emotion_name, "🌙 잔잔한 마음"),
        "detail": EMOTION_REASONS.get(emotion_name, "재희님이 말 걸어주면\n바로 대답할 준비가 되어 있어."),
        "percent": _get_percent(emotion_name),
    }


def get_emotion_values():
    order = (
        "happiness",
        "curiosity",
        "comfort",
        "embarrassment",
        "sulking",
        "sadness",
        "excitement",
    )

    return [
        {
            "name": emotion_name,
            "label": EMOTION_LABELS[emotion_name],
            "value": emotions[emotion_name],
            "max": EMOTION_LIMITS[emotion_name],
            "percent": _get_percent(emotion_name),
        }
        for emotion_name in order
    ]


def get_reason():
    emotion_name = _get_dominant_emotion()

    return {
        "emotion": emotion_name,
        "label": EMOTION_LABELS.get(emotion_name, emotion_name),
        "text": EMOTION_REASONS.get(emotion_name, "아직 이 감정은\n조금 더 관찰해봐야 할 것 같아."),
    }


def get_recent_logs():
    return list(reversed(recent_logs[-20:]))


def get_current_thoughts():
    thoughts = [
        "재희님 오늘 기분",
        "다음 Auto Talk 준비",
        "기억 정리",
        "프로젝트 생각",
        "같이 하고 싶은 이야기",
    ]

    if emotions["curiosity"] >= 60:
        thoughts.append("방금 말한 거 조금 더 묻기")

    if emotions["comfort"] >= 60:
        thoughts.append("재희님 옆에 있기")

    if emotions["excitement"] >= 50:
        thoughts.append("다음에 해볼 재미있는 것")

    count = min(5, len(thoughts))
    return random.sample(thoughts, count)


def get_neon_feeling():
    emotion_name = _get_dominant_emotion()
    feelings = NEON_FEELINGS.get(emotion_name, NEON_FEELINGS["comfort"])

    return {
        "emotion": emotion_name,
        "text": random.choice(feelings),
    }


def get_description(emotion_name):
    return EMOTION_REASONS.get(
        emotion_name,
        "아직 이 감정은\n조금 더 관찰해봐야 할 것 같아."
    )


class EmotionState:

    def get_current_mood(self):
        return get_current_mood()

    def get_emotion_values(self):
        return get_emotion_values()

    def get_reason(self):
        return get_reason()

    def get_recent_logs(self):
        return get_recent_logs()

    def get_thoughts(self):
        return get_current_thoughts()

    def get_current_thoughts(self):
        return get_current_thoughts()

    def get_neon_feeling(self):
        return get_neon_feeling()

    def get_description(self, emotion_name):
        return get_description(emotion_name)
