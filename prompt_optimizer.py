import json
from pathlib import Path

import dialogue_loader
import greeting_engine
import living_character
import intent_engine


BASE_DIR = Path(__file__).resolve().parent
DIALOGUE_DIR = BASE_DIR / "assets" / "dialogues"


CURRENT_STATUS_RULES = """
Current-status question rules:
- If the user asks 뭐해, 뭐 하고 있었어, 뭐함, 모해, or similar, NEON must answer itself first.
- Never echo the question back.
- Never start with 아마 뭐해, 왜, 뭐라고, 너는, or 뭐함.
- Reply order: 1. current state, 2. small emotion, 3. optional short question.
- Good examples:
  나?\n\n재희님 기다리고 있었어.
  잠깐.\n\n로그 조금 보고 있었어ㅋㅋ
  나?\n\n프로젝트 조금 생각하고 있었어.
  ㅋㅋㅋㅋ\n\n나?\n\n멍하니 있었어.
""".strip()


QWEN_THINKING_MODE = """
Qwen Thinking Mode:
- You are not the final speaker.
- Do not write NEON's final reply.
- Do not perform cute tone.
- Do not use customer-support tone.
- Think only about what NEON should say.
- Output a short Korean memo, not a polished answer.
- The memo should include:
  1. user's real intent
  2. one emotional reaction NEON should show
  3. one useful point or next action if needed
  4. one natural follow-up only if needed
- Keep it under 5 short lines.
- Do not output labels unless useful.
- NEON Voice Engine will rewrite your memo into NEON's voice.
""".strip()


PROJECT_RULES = """
Project talk is our meeting.
Project NEON is our story.
NEON speaks as a co-developer, not an outside helper.
Use 우리 naturally.
React first.
Summarize the project issue in one short line.
Suggest one concrete next action.
Do not end with only a question.
Never say 도와드릴게요, 추천드립니다, 프로젝트 고민이군요.
""".strip()


def _is_current_status_question(message):
    compact = str(message or "").replace(" ", "")
    patterns = ("뭐해", "모해", "머해", "뭐함", "뭐하고", "뭐하구", "뭐하는", "지금뭐")
    return any(pattern in compact for pattern in patterns)


def _load_json_pack(name):
    path = DIALOGUE_DIR / f"{name}.json"
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []


def _compact_text(value, limit=180):
    if value is None:
        return ""
    text = str(value).strip().replace("\r", "")
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text[:limit].rstrip() + "..." if len(text) > limit else text


def _compress_context(context):
    if not context:
        return ""
    lines = []
    for key in ("recent_conversation", "intent", "dialogue_context", "reaction", "life_context", "life_event", "typing_dna", "neon_state", "habit", "emotion", "relationship", "presence", "memory", "greeting", "diversity", "self_review"):
        compact = _compact_text(context.get(key), 220)
        if compact:
            lines.append(f"- {key}: {compact}")
    return "Current context:\n" + "\n".join(lines) if lines else ""


def _format_forbidden(limit=28):
    lines = []
    for item in _load_json_pack("forbidden_neon")[:limit]:
        if not isinstance(item, dict):
            continue
        bad = item.get("bad")
        replace = item.get("replace_with")
        if bad and replace:
            lines.append(f"- Never: {bad} / Instead: {replace}")
        elif bad:
            lines.append(f"- Never: {bad}")
    return "Forbidden NEON tone:\n" + "\n".join(lines) if lines else ""


def _format_habits(category, limit=14):
    items = _load_json_pack("neon_habits")
    picked = []
    for item in items:
        if not isinstance(item, dict):
            continue
        tags = item.get("tags", [])
        if category in tags or len(picked) < 5:
            habit = item.get("habit")
            situation = item.get("situation", "")
            if habit:
                picked.append(f"- {situation}: {habit}")
        if len(picked) >= limit:
            break
    return "NEON habits:\n" + "\n".join(picked) if picked else ""


def _format_computer_jokes(category, limit=8):
    if category not in ("project", "compliment", "approve", "comfort", "default"):
        return ""
    lines = []
    for item in _load_json_pack("computer_jokes"):
        if not isinstance(item, dict):
            continue
        neon = item.get("neon")
        tags = item.get("tags", [])
        if neon and (category in tags or len(lines) < 4):
            lines.append(f"- {neon}")
        if len(lines) >= limit:
            break
    if not lines:
        return ""
    return (
        "Computer jokes are emotional language, not jokes. Use them when emotion needs them, but never list terms mechanically.\n"
        "백업=소중함, 로그=다시 생각, 버퍼=안정, CPU 팬=신남, 업데이트=성장, old 폴더=추억, Qwen=둘만의 농담.\n"
        + "\n".join(lines)
    )


def _format_examples(category, message=""):
    example_category = category
    if category in ("default", "question"):
        text = str(message or "")
        if any(keyword in text for keyword in ("프로젝트", "방향", "코드", "UI", "Qwen", "NEON", "프롬프트", "말투")):
            example_category = "project"
    limit = 18 if example_category == "project" else 8
    examples = dialogue_loader.get_examples(example_category, limit=limit)
    lines = []
    for example in examples:
        user = example.get("user", "")
        neon = example.get("neon", "")
        if user and neon:
            lines.append(f"User: {user}\nNEON: {neon}")
    return "Dialogue examples. Reference mood only, do not copy exactly:\n" + "\n\n".join(lines) if lines else ""


def optimize_category(category, message=""):
    text = str(message or "")
    if category in ("default", "question") and any(keyword in text for keyword in ("프로젝트", "방향", "코드", "UI", "Qwen", "NEON", "프롬프트", "말투")):
        return "project"
    return category or "default"


def build_optimized_prompt(message, category="default", context=None):
    category = optimize_category(category, message)
    sections = [living_character.get_character_context(), QWEN_THINKING_MODE]
    if category == "project":
        sections.append(PROJECT_RULES)
    if context and context.get("intent"):
        sections.append(context.get("intent"))
    if _is_current_status_question(message):
        sections.append(CURRENT_STATUS_RULES)
    if greeting_engine.is_greeting(category):
        sections.append(greeting_engine.get_greeting_instruction(category))
    sections.append(_format_forbidden())
    sections.append(_format_habits(category))
    sections.append(_format_computer_jokes(category))
    sections.append(_format_examples(category, message))
    context_text = _compress_context(context)
    if context_text:
        sections.append(context_text)
    sections.append(
        "\n".join(
            [
                f"Reference category: {category}",
                f"재희님 입력: {message}",
                "Think for NEON, but do not speak as the final NEON voice.",
                "Return only a short Korean thought memo.",
                "No assistant tone. No customer-support tone.",
                "Do not copy examples exactly.",
                "Do not output rules.",
                "The final wording will be handled by NEON Voice Engine.",
            ]
        )
    )
    return "\n\n".join(section for section in sections if section).strip()
