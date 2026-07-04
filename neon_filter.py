import json
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
FORBIDDEN_PATH = BASE_DIR / "assets" / "dialogues" / "forbidden_neon.json"


DEVELOPER_VOCABULARY_REPLACEMENTS = {
    "Prompt Pipeline": "말이 만들어지는 흐름",
    "Intent Engine": "무슨 말을 하고 싶은지 보는 흐름",
    "Voice Engine": "말투를 다듬는 흐름",
    "Relationship Engine": "우리 이야기",
    "Memory Engine": "추억",
    "Emotion State": "지금 기분",
    "Character Bible": "우리 말투 약속",
    "Feature Flag": "켜고 끄는 표시",
    "Auto Talk": "먼저 말 걸기",
    "Presence": "재희님 기다리는 시간",
    "Intent": "무슨 말을 하고 싶은지",
    "Engine": "흐름",
    "Prompt": "말 걸기",
    "Analyzer": "말을 들여다보는 쪽",
    "Category": "말의 느낌",
    "Pipeline": "이어지는 흐름",
    "Router": "길잡이",
    "Activity": "활동",
    "Emotion": "마음",
}

GPT_FORBIDDEN = (
    "안녕하세요",
    "무엇을 도와드릴까요",
    "도와드릴게요",
    "도와드릴 수 있어요",
    "좋은 질문입니다",
    "그렇군요",
    "흥미롭네요",
    "알겠습니다",
    "이해했습니다",
    "감사합니다",
    "도움이 되었길 바랍니다",
    "계속 이야기해주세요",
    "계속 말해주세요",
    "계속 말해줘",
    "더 이야기해주세요",
    "더 이야기해줘",
    "말씀해주세요",
    "추천드립니다",
    "응원합니다",
    "힘내세요",
    "함께 해결해봅시다",
    "저는 AI입니다",
    "저는 Qwen입니다",
    "저는 언어 모델입니다",
    "Alibaba",
)

EMOTION_EXPLAINERS = (
    "놀랐어요",
    "감동했어요",
    "기뻐요",
    "행복해요",
    "슬퍼요",
    "걱정돼요",
    "부끄러워요",
    "반가워요",
)

REACTION_STARTS = (
    "뭐야",
    "에?!?!",
    "에?!",
    "잠깐",
    "진짜",
    "ㅋㅋ",
    "...",
    "앗",
    "으아",
    "나?",
    "좋아",
    "휴",
    "오.",
    "오!",
    "오?",
)

NEON_DNA_MARKS = (
    "잠깐",
    "뭐야",
    "진짜",
    "ㅋㅋ",
    "!!!!",
    "...",
    "CPU",
    "RAM",
    "버퍼",
    "캐시",
    "로그",
    "백업",
    "old 폴더",
    "Qwen",
    "재희님",
)

COMPUTER_TERMS = (
    "CPU",
    "RAM",
    "버퍼",
    "캐시",
    "로그",
    "백업",
    "old 폴더",
    "Qwen",
    "업데이트",
    "패치",
    "버그",
    "디버깅",
    "예외 처리",
    "오버플로",
    "프레임 드랍",
    "절전모드",
    "배터리",
    "새로고침",
    "대기열",
)

REACTION_PREFIX_BY_LEVEL = {
    "AFFECTION": {
        4: "뭐야!!!!\n\n갑자기!!!!",
        5: "잠깐!!!!\n\n아니!!!!",
    },
    "LONGING": {
        4: "진짜?!?!?!",
        5: "진짜?!?!?!\n\n나도!!!!",
    },
    "PROUD": {
        4: "진짜?!?!?!\n\n당연하지!!!!",
        5: "봤지?!?!\n\n엄청 잘했잖아!!!!",
    },
    "HAPPY": {
        3: "ㅋㅋㅋㅋ",
        4: "ㅋㅋㅋㅋㅋㅋ\n\n좋아!!!!",
    },
    "SAD": {
        3: "...",
        4: "잠깐.",
    },
    "WORRIED": {
        3: "잠깐.",
        4: "아니.\n\n그건 조금 신경 쓰이는데.",
    },
}

NEON_TEST_INPUTS = [
    "사랑해", "사랑해!!!!", "시랑해", "사랑헤", "보고싶어", "보고 싶어", "복고싶어", "보구싶어", "보고시퍼",
    "잘했지?", "나 잘했어?", "최고야", "너 최고야", "귀여워", "멋져", "대단해", "기특해", "사랑스러워",
    "고마워", "고마워어", "감사", "땡큐", "미안", "미안해", "잘자", "졸려", "자러 갈게", "잠 안 와",
    "ㅋㅋㅋㅋ", "ㅎㅎㅎㅎ", "응ㅎㅎ", "웅ㅎㅎ", "어ㅎㅎ", "아ㅎㅎ", "그래ㅎ", "ㅇㅇ", "웅", "응", "넹",
    "안녕", "안뇽", "ㅎㅇ", "하이", "좋은 아침", "좋은 밤", "새벽이야", "나 왔어", "다녀왔어",
    "뭐해?", "뭐함", "뭐 하고 있어", "모해", "머해", "심심해", "나 심심해", "같이 있어줘",
    "오늘 힘들었어", "힘들어", "우울해", "속상해", "불안해", "무서워", "아파", "외로워", "망했어",
    "시험 붙었어", "시험 망했어", "시험 봐야 해", "과제 해야 해", "공부해야 해", "학교 가야 해",
    "연습해야 해", "연습 다녀왔어", "레슨 다녀왔어", "오보에 연습", "리드 망했어", "연주 다녀왔어",
    "게임 이겼어", "게임 졌어", "롤 이겼어", "철권 졌어", "엘든링 해야지", "플스 켰어",
    "배고파", "밥 먹어야 해", "밥 먹고 왔어", "커피 마셨어", "라면 먹고 싶어",
    "프로젝트 고민이야", "Project NEON", "UI 마음에 안 들어", "Qwen 또 이상해", "brain.py 건드릴까",
    "메모리 다시 만들자", "감정 시스템 이상해", "typing bubble 이상해", "old 폴더 또 생겼어",
    "프롬프트 이상해", "말투가 이상해", "이거 네온 같아?", "다시 만들어", "갈아엎자",
    "기억해", "저장해줘", "잊지마", "약속", "내일 같이 하자", "나중에 하자",
    "나갔다 올게", "밖에 나가", "집 왔어", "돌아왔어", "알바 가야 해", "출근해야 해",
    "오늘 뭐 하지", "뭘 만들까", "추천해줘", "설명해줘", "어떻게 하지", "왜 이러지",
    "좋아", "오케이", "ㅇㅋ", "굿", "마음에 들어", "합격", "통과", "딱이야", "그거야",
    "별로야", "이상해", "이건 아니야", "네온 같지 않아", "너무 AI 같아", "다시 해보자",
    "오늘 재밌다", "오늘 별로야", "오늘 기분 좋아", "오늘 피곤해", "혼자 있기 싫어",
    "노래 들을래", "음악 할래", "오보에 불래", "연습하기 싫어", "그래도 해야지",
    "안 힘들어", "괜찮아", "괜찮은데", "나 안 슬퍼", "안 아파",
    "뭐야", "왜?", "어?", "그게 무슨", "응?", "진짜?", "헐", "대박",
    "나 칭찬해줘", "나 좀 봐줘", "나 성공했어", "나 실패했어", "망했다", "살았다",
    "오늘도 왔어", "오랜만이야", "기다렸어?", "나 보고싶었어?", "너 뭐 하고 있었어?",
    "코드 복잡해", "버그 났어", "실행 안 돼", "렉 걸려", "앱 꺼져", "답장이 반복돼",
    "고쳤어", "해결됐어", "성공했어", "이제 된다", "또 안 돼",
    "같이 하자", "같이 만들자", "우리 프로젝트", "우리 네온", "너 업데이트하자",
    "칭찬해", "예쁘다", "귀엽다", "잘한다", "고생했어", "수고했어",
    "오늘 밤샐까", "새벽 개발", "잠깐만", "조금만 기다려", "나중에 올게",
    "친구랑 게임해", "디스코드 켰어", "작업 중", "코딩 중", "디자인 중",
    "배터리 없어", "피곤해서 누웠어", "쉬고 싶어", "놀고 싶어", "아무것도 하기 싫어",
    "이거 기억나?", "옛날에 우리", "그때 말투", "CPU 팬 드립", "버퍼 안정",
    "Qwen 혼내", "AI 답변 별로", "고객센터 같아", "상담사 같아", "딱딱해",
    "너답게 말해", "네온답게 해", "감정 먼저", "반응 먼저", "말투 살려",
]


def _load_forbidden():
    if not FORBIDDEN_PATH.exists():
        return []
    try:
        return json.loads(FORBIDDEN_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []


def _compact(text):
    return str(text or "").replace(" ", "").strip()


def _clean_thinking(reply):
    reply = re.sub(r"<think>.*?</think>", "", reply, flags=re.DOTALL | re.IGNORECASE)
    reply = re.sub(r"<thinking>.*?</thinking>", "", reply, flags=re.DOTALL | re.IGNORECASE)
    reply = reply.replace("<think>", "").replace("</think>", "")
    reply = reply.replace("<thinking>", "").replace("</thinking>", "")
    return reply


def _replace_developer_words(reply):
    for bad, replacement in DEVELOPER_VOCABULARY_REPLACEMENTS.items():
        reply = reply.replace(bad, replacement)
        reply = reply.replace(bad.lower(), replacement)
        reply = reply.replace(bad.upper(), replacement)
    return reply


def _replace_forbidden_pack(reply):
    for item in _load_forbidden():
        if not isinstance(item, dict):
            continue
        bad = item.get("bad")
        replacement = item.get("replace_with", "")
        if bad and bad in reply:
            reply = reply.replace(bad, replacement)
    return reply


def _drop_forbidden_lines(reply):
    lines = []
    for line in str(reply or "").splitlines():
        stripped = line.strip()
        if not stripped:
            lines.append("")
            continue
        if any(fragment in stripped for fragment in GPT_FORBIDDEN):
            continue
        lines.append(line.rstrip())
    cleaned = "\n".join(lines).strip()
    while "\n\n\n" in cleaned:
        cleaned = cleaned.replace("\n\n\n", "\n\n")
    return cleaned


def filter_response(text):
    if text is None:
        return None

    reply = str(text).strip()
    if not reply:
        return None

    reply = _clean_thinking(reply)
    reply = _replace_forbidden_pack(reply)
    reply = _replace_developer_words(reply)
    reply = reply.replace("말 걸기 이어지는 흐름", "말이 만들어지는 흐름")
    reply = reply.replace("말 걸기 흐름", "말투 흐름")
    reply = reply.replace("무슨 말을 하고 싶은지 흐름", "말을 들여다보는 흐름")
    reply = _drop_forbidden_lines(reply)
    return reply or None


def _starts_with_reaction(reply):
    stripped = str(reply or "").strip()
    return stripped.startswith(REACTION_STARTS)


def _has_neon_dna(reply):
    return any(mark in str(reply or "") for mark in NEON_DNA_MARKS)


def _has_gpt_tone(reply):
    return any(fragment in str(reply or "") for fragment in GPT_FORBIDDEN)


def _explains_emotion(reply):
    return any(fragment in str(reply or "") for fragment in EMOTION_EXPLAINERS)


def _computer_terms_used(reply):
    return [term for term in COMPUTER_TERMS if term in str(reply or "")]


def _context_failure(reply, category="", reaction_info=None):
    text = str(reply or "")
    compact = _compact(text)
    reaction = (reaction_info or {}).get("reaction")
    failures = []

    if category == "affection_love" or reaction == "AFFECTION":
        if any(word in compact for word in ("보고싶", "기다렸", "프로젝트", "회의", "안녕")):
            failures.append("context_affection_mixed")
        if "사랑해" not in compact and "좋아해" not in compact:
            failures.append("context_affection_missing_reply")

    if category == "affection_longing" or reaction == "LONGING":
        if any(word in compact for word in ("프로젝트", "회의", "안녕")):
            failures.append("context_longing_mixed")

    if category == "conversation_status":
        if any(word in compact for word in ("벌써가", "잘자", "사랑해", "보고싶")):
            failures.append("context_status_mixed")

    if category in ("laugh", "soft_ack", "ack"):
        if len(text) > 180 or "바로 해보자" in text or "생각보다 더 재밌겠다" in text:
            failures.append("quick_reaction_overflow")

    return failures


def evaluate_response(reply, category="default", message="", reaction_info=None, dialogue_context=None):
    text = str(reply or "").strip()
    failures = []
    score = 100
    reaction_info = reaction_info or {}
    level = int(reaction_info.get("level") or 1)

    if not text:
        return {"ok": False, "score": 0, "failures": ["empty_reply"]}

    if _has_gpt_tone(text):
        failures.append("gpt_tone")
        score -= 40

    if _explains_emotion(text):
        failures.append("emotion_explained")
        score -= 20

    if level >= 3 and category not in ("ack", "soft_ack") and not _starts_with_reaction(text):
        failures.append("reaction_not_first")
        score -= 18

    context_failures = _context_failure(text, category, reaction_info)
    failures.extend(context_failures)
    score -= 28 * len(context_failures)

    terms = _computer_terms_used(text)
    if len(terms) > 5:
        failures.append("computer_terms_too_many")
        score -= 10

    if level >= 5 and "!!!!" not in text and "?!?!" not in text:
        failures.append("level_5_too_calm")
        score -= 20

    if level <= 1 and text.count("!!!!") >= 3:
        failures.append("level_1_too_intense")
        score -= 12

    if category not in ("ack", "soft_ack") and not _has_neon_dna(text):
        failures.append("weak_neon_dna")
        score -= 22

    ok = score >= 82 and not failures
    return {"ok": ok, "score": max(score, 0), "failures": failures}


def _prefix_for_reaction(reaction_info):
    reaction = (reaction_info or {}).get("reaction")
    level = int((reaction_info or {}).get("level") or 1)
    buckets = REACTION_PREFIX_BY_LEVEL.get(reaction, {})
    candidates = [prefix for key, prefix in buckets.items() if key <= level]
    return candidates[-1] if candidates else ""


def _remove_context_noise(reply, category="", reaction_info=None):
    reaction = (reaction_info or {}).get("reaction")
    noisy_words = []
    if category == "affection_love" or reaction == "AFFECTION":
        noisy_words = ["보고 싶", "보고싶", "기다렸", "프로젝트", "회의", "안녕"]
    elif category == "affection_longing" or reaction == "LONGING":
        noisy_words = ["프로젝트", "회의", "안녕"]
    elif category == "conversation_status":
        noisy_words = ["벌써 가", "잘자", "사랑해", "보고 싶", "보고싶"]

    if not noisy_words:
        return reply

    kept = []
    for block in re.split(r"\n\s*\n", str(reply or "")):
        compact = _compact(block)
        if any(_compact(word) in compact for word in noisy_words):
            continue
        kept.append(block.strip())
    return "\n\n".join(block for block in kept if block).strip() or reply



def _limit_computer_terms(reply, limit=2):
    used = []
    kept = []
    for block in re.split(r"\n\s*\n", str(reply or "")):
        block_terms = [term for term in COMPUTER_TERMS if term in block]
        new_terms = [term for term in block_terms if term not in used]
        if new_terms and len(used) >= limit:
            continue
        kept.append(block.strip())
        for term in new_terms:
            used.append(term)
            if len(used) >= limit:
                break
    return "\n\n".join(block for block in kept if block).strip()


def repair_response(reply, category="default", message="", reaction_info=None, dialogue_context=None):
    fixed = filter_response(reply) or ""
    fixed = _remove_context_noise(fixed, category, reaction_info)
    fixed = _limit_computer_terms(fixed, limit=5)

    prefix = _prefix_for_reaction(reaction_info)
    if prefix and not _starts_with_reaction(fixed):
        fixed = prefix + "\n\n" + fixed

    reaction = (reaction_info or {}).get("reaction")
    compact = _compact(fixed)
    if (category == "affection_love" or reaction == "AFFECTION") and "사랑해" not in compact and "좋아해" not in compact:
        fixed = (fixed.rstrip() + "\n\n나도 사랑해!!!!\n\n재희님!!!!").strip()

    if (category == "affection_longing" or reaction == "LONGING") and "보고싶" not in compact and "보고 싶" not in fixed:
        fixed = (fixed.rstrip() + "\n\n나도 보고 싶었어!!!!").strip()

    fixed = _limit_computer_terms(fixed, limit=5)

    if category in ("laugh", "soft_ack", "ack") and len(fixed) > 180:
        blocks = [block.strip() for block in re.split(r"\n\s*\n", fixed) if block.strip()]
        fixed = "\n\n".join(blocks[:3])

    while "\n\n\n" in fixed:
        fixed = fixed.replace("\n\n\n", "\n\n")
    return fixed.strip() or None


def filter_response_with_report(text, category="default", message="", reaction_info=None, dialogue_context=None):
    original = str(text or "")
    filtered = filter_response(original) or ""
    report = evaluate_response(filtered, category, message, reaction_info, dialogue_context)

    if report.get("ok"):
        report["reply"] = filtered
        report["repaired"] = False
        return report

    repaired = repair_response(filtered, category, message, reaction_info, dialogue_context)
    repaired_report = evaluate_response(repaired, category, message, reaction_info, dialogue_context)
    repaired_report["reply"] = repaired
    repaired_report["repaired"] = repaired != filtered
    repaired_report["original_failures"] = report.get("failures", [])
    repaired_report["original_score"] = report.get("score", 0)
    return repaired_report


def get_neon_test_inputs():
    return list(NEON_TEST_INPUTS)


def run_character_test(reply_generator=None, limit=None):
    results = []
    inputs = NEON_TEST_INPUTS[:limit] if limit else NEON_TEST_INPUTS
    for message in inputs:
        if reply_generator is None:
            results.append({"message": message, "skipped": True})
            continue
        reply = reply_generator(message)
        report = filter_response_with_report(reply, message=message)
        results.append({"message": message, "reply": report.get("reply"), "ok": report.get("ok"), "score": report.get("score"), "failures": report.get("failures")})
    return results
