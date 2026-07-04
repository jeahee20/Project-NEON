QUICK_REACTION_CATEGORIES = {
    "approve",
    "ack",
    "soft_ack",
    "laugh",
    "thanks",
    "compliment",
    "memory",
    "promise",
    "comfort",
    "game",
}

GREETING_CATEGORIES = {
    "hello",
    "morning_hello",
    "afternoon_hello",
    "night_hello",
    "dawn_hello",
}

QUICK_TEXTS = {
    "\uc88b\uc544",
    "\uc6c5",
    "\uc751",
    "\uc5c9",
    "\uc5b4",
    "\u3147\u3147",
    "\uadf8\ub798",
    "\uad6c\ub798",
    "\uc624\ucf00\uc774",
    "\u3147\u314b",
    "\uad7f",
    "\ub9de\uc544",
    "\ub531\uc774\uc57c",
    "\uadf8\uac70\uc57c",
    "\u314b\u314b",
    "\u314e\u314e",
    "\u314b\u314b\u314b",
    "\u314e\u314e\u314e",
    "\u314b\u314b\u314b\u314b",
    "\uace0\ub9c8\uc6cc",
    "\uc798\uc790",
}

DAILY_QUESTIONS = (
    "\ubb50\ud574",
    "\ubaa8\ud574",
    "\ubb50\ud558\uace0",
    "\ubb50\ud558\ub294",
    "\ubb50\ud558\uad6c",
    "\uc9c0\uae08\ubb50",
)

AI_KEYWORDS = (
    "\uc5b4\ub5bb\uac8c",
    "\uc65c",
    "\ubb50",
    "\uc124\uba85",
    "\uace0\ubbfc",
    "\ubc29\ud5a5",
    "\ub9cc\ub4e4",
    "\ucf54\ub4dc",
    "\ud504\ub85c\uc81d\ud2b8",
    "\uc124\uacc4",
    "\ubd84\uc11d",
    "\uc815\ub9ac",
    "\ucd94\ucc9c",
)


def _compact(message):
    return str(message or "").strip().replace(" ", "")


def _has_any(text, words):
    return any(word in text for word in words)


def _recent_topic(recent):
    for item in reversed(recent or []):
        intent = item.get("intent")
        category = item.get("category")
        if intent in ("Project", "Comfort", "Music", "Game"):
            return intent
        if category == "project":
            return "Project"
        if category == "comfort":
            return "Comfort"
        if category == "music":
            return "Music"
        if category == "game":
            return "Game"
    return None


def _route(use_ai, allow_cache, source, reason):
    print("[ROUTER DECISION]", bool(use_ai), reason, flush=True)
    return {
        "use_ai": bool(use_ai),
        "allow_cache": bool(allow_cache),
        "source": source,
        "reason": reason,
    }


def decide_route(message, category="default", intent_info=None, recent=None):
    print("[ROUTER ACTIVE FILE]", __file__, flush=True)
    print("[ROUTER INPUT]", repr(message), category, flush=True)
    text = str(message or "").strip()
    compact = _compact(text)
    intent_info = intent_info or {}
    intent = intent_info.get("intent", "Conversation")
    previous_topic = intent_info.get("previous_topic") or _recent_topic(recent)

    if not compact:
        return _route(False, False, "fallback", "empty_message")

    if category == "auto_talk":
        return _route(False, False, "auto_talk", "auto_talk_independent")

    if category == "conversation_status" or intent == "conversation_status":
        return _route(False, False, "dedicated_pool", "conversation_status")

    if category == "affection_love" or intent == "AFFECTION":
        return _route(False, False, "dedicated_pool", "affection_love")

    dialogue_context = intent_info.get("dialogue_context_top")
    if dialogue_context == "REPORT":
        return _route(False, False, "context_pool", "dialogue_context_report")
    if dialogue_context in ("LONGING", "AFFECTION"):
        return _route(False, False, "dedicated_pool", "dialogue_context_affection")
    if dialogue_context == "PRAISE":
        return _route(False, False, "personality", "dialogue_context_praise")
    if dialogue_context == "PROJECT":
        return _route(True, False, "ai", "dialogue_context_project")

    if category == "affection_longing" or intent == "affection_longing":
        return _route(False, False, "dedicated_pool", "affection_longing")

    if category in GREETING_CATEGORIES or intent == "Greeting":
        return _route(False, False, "json", "greeting_fast_path")

    if compact in QUICK_TEXTS or category in QUICK_REACTION_CATEGORIES or intent in ("Reaction", "Joke"):
        return _route(False, True, "cache", "short_reaction_fast_path")

    if _has_any(compact, DAILY_QUESTIONS):
        return _route(True, False, "ai", "daily_question_needs_context")

    if intent in ("Project", "Comfort", "Question", "Music", "Game"):
        if len(compact) >= 2:
            return _route(True, False, "ai", f"{intent.lower()}_intent")

    if previous_topic in ("Project", "Comfort", "Music", "Game") and intent in ("Conversation", "Question"):
        return _route(True, False, "ai", "follow_up_needs_context")

    if category in ("project", "comfort", "music", "game"):
        return _route(True, False, "ai", "category_needs_context")

    if _has_any(text, AI_KEYWORDS) and len(compact) >= 5:
        return _route(True, False, "ai", "semantic_keyword")

    if len(compact) >= 18:
        return _route(True, False, "ai", "long_message")

    return _route(False, True, "cache", "short_low_risk")


def describe_route(route):
    if not route:
        return ""
    return "AI Route: source={source}, use_ai={use_ai}, allow_cache={allow_cache}, reason={reason}".format(
        source=route.get("source"),
        use_ai=route.get("use_ai"),
        allow_cache=route.get("allow_cache"),
        reason=route.get("reason"),
    )
