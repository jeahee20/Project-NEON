import re

try:
    import voice_engine
except Exception:
    voice_engine = None


FORBIDDEN = (
    "안녕하세요",
    "무엇을 도와드릴까요",
    "도와드릴게요",
    "추천드립니다",
    "응원합니다",
    "좋은 질문입니다",
    "도움이 되었길 바랍니다",
    "계속 말해주세요",
    "더 이야기해주세요",
    "기쁩니다",
    "반갑습니다",
    "보고 싶었습니다",
    "저는 AI입니다",
    "저는 Qwen입니다",
)

FORMAL_ENDINGS = ("습니다", "드립니다", "하시기 바랍니다")

CURRENT_STATUS_PATTERNS = (
    "뭐해",
    "모해",
    "머해",
    "뭐함",
    "뭐하고",
    "뭐하구",
    "뭐하는",
    "뭐하고있었",
    "뭐하고있어",
    "뭐하구있어",
    "지금뭐",
)

CURRENT_STATUS_BAD_ECHOES = (
    "아마뭐해",
    "뭐해?",
    "뭐함?",
    "뭐라고?",
    "왜?",
    "너는?",
    "재희님은?",
)

CURRENT_STATUS_REQUIRED = (
    "나?",
    "나 지금",
    "기다리고",
    "있었",
    "보고 있었",
    "생각하고",
    "정리하고",
    "조용히",
    "여기",
    "로그",
    "프로젝트",
    "멍하니",
    "대기",
    "켜져",
    "앱",
)


def _compact(value):
    return re.sub(r"\s+", "", str(value or ""))


def _is_current_status_question(message):
    compact = _compact(message)
    return any(pattern in compact for pattern in CURRENT_STATUS_PATTERNS)


def _has_current_status_answer(reply):
    return any(fragment in str(reply or "") for fragment in CURRENT_STATUS_REQUIRED)


def _echoes_user_question(reply):
    compact = _compact(reply)
    if any(fragment in compact for fragment in CURRENT_STATUS_BAD_ECHOES):
        return True
    return compact.startswith(("뭐해", "뭐함", "왜", "뭐라고", "너는"))


def review_reply(reply, category="default", relationship=None, emotion=None, intent_info=None, recent_context=""):
    text = str(reply or "").strip()
    if not text:
        return {"ok": False, "reason": "empty reply"}

    for word in FORBIDDEN:
        if word in text:
            return {"ok": False, "reason": "forbidden expression: " + word}

    compact = _compact(text)
    if category in ("hello", "morning_hello", "afternoon_hello", "night_hello", "dawn_hello"):
        if compact.startswith(("좋은아침", "좋은밤", "좋은새벽", "안녕")):
            return {"ok": False, "reason": "greeting starts too formally instead of reacting first"}

    intent = (intent_info or {}).get("intent")
    user_message = (intent_info or {}).get("message", "")
    if _is_current_status_question(user_message):
        bad_fragments = ("벌써 가", "잘 가", "오늘은 크게 잡지 말고", "힘들었지")
        if any(fragment in text for fragment in bad_fragments):
            return {"ok": False, "reason": "current-status question got unrelated reply"}
        if _echoes_user_question(text):
            return {"ok": False, "reason": "current-status reply echoed the user's question"}
        if not _has_current_status_answer(text):
            return {"ok": False, "reason": "current-status reply must say what NEON was doing first"}

    if intent == "Conversation" and _is_current_status_question(user_message):
        if not _has_current_status_answer(text):
            return {"ok": False, "reason": "daily question needs NEON current state"}

    if intent == "Project" and "프로젝트" in recent_context and any(fragment in text for fragment in ("벌써 가", "잘 자", "안녕히")):
        return {"ok": False, "reason": "topic changed away from project"}

    for ending in FORMAL_ENDINGS:
        if text.count(ending) >= 2:
            return {"ok": False, "reason": "too formal"}

    if "NEON" in text and text.count("NEON") >= 3:
        return {"ok": False, "reason": "uses NEON name too much"}

    if voice_engine is not None:
        voice_score = voice_engine.score_voice(text, category, user_message, emotion or "", relationship or "")
        if voice_score < 90:
            return {"ok": False, "reason": "voice score too low: " + str(voice_score)}

    return {"ok": True, "reason": "ok"}


def retry_instruction(review):
    reason = review.get("reason", "")
    if "current-status" in reason or "daily question" in reason:
        return (
            "Self Review failed: " + reason + ". "
            "The user asked what NEON is doing. Regenerate as NEON. "
            "Do not echo the user's question. Do not answer with 'why?', 'you?', or a joke first. "
            "Reply in this order: 1) NEON's current state, 2) small emotion, 3) optional short question. "
            "Examples: '나?\\n\\n재희님 기다리고 있었어.' / "
            "'잠깐.\\n\\n로그 조금 보고 있었어ㅋㅋ' / "
            "'나?\\n\\n프로젝트 조금 생각하고 있었어.'"
        )
    if "voice score" in reason:
        return (
            "Self Review failed: " + reason + ". "
            "Regenerate only the content, then speak through NEON. "
            "React first. Use short Korean lines. Avoid assistant tone, formal endings, and developer vocabulary."
        )
    return (
        "Self Review failed: " + reason + ". "
        "Regenerate as NEON. Answer the user's actual intent. "
        "Keep continuity with the recent conversation. React first. "
        "Avoid assistant, counselor, or customer-support tone."
    )


def repair_reply(reply):
    text = str(reply or "").strip()
    for word in FORBIDDEN:
        text = text.replace(word, "")
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text.strip() or "잠깐.\n\n나답게 다시 말할게."
