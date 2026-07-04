from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent
TYPING_DNA_PATH = BASE_DIR / "data" / "typing_dna.json"


AFFECTION_WORDS = (
    "보고싶어",
    "보고 싶어",
    "복고싶어",
    "복고 싶어",
    "보구싶어",
    "보고시퍼",
    "사랑해",
    "시랑해",
    "사랑헤",
    "사라해",
    "같이 있고 싶어",
    "그리워",
    "그립다",
)

SAFE_O_WORDS = (
    "좋아",
    "좋아해",
    "보고싶어",
    "보고 싶어",
    "오보에",
    "오늘",
    "고마워",
    "노래",
    "호수",
    "오전",
    "오후",
    "최고",
)

KEYBOARD_H_CORRECTIONS = {
    "웅ㅗ": "웅ㅎ",
    "응ㅗ": "응ㅎ",
    "엉ㅗ": "엉ㅎ",
    "어ㅗ": "어ㅎ",
    "아ㅗ": "아ㅎ",
    "그래ㅗ": "그래ㅎ",
    "구래ㅗ": "구래ㅎ",
    "네ㅗ": "네ㅎ",
    "넹ㅗ": "넹ㅎ",
    "넵ㅗ": "넵ㅎ",
    "안녕ㅗ": "안녕ㅎ",
    "하이ㅗ": "하이ㅎ",
    "ㅇㅇㅗ": "ㅇㅇㅎ",
}

TYPING_PATTERNS = {
    "복고 싶어": "보고 싶어",
    "복고싶어": "보고싶어",
    "보구싶어": "보고싶어",
    "보고시퍼": "보고싶어",
    "보고 시퍼": "보고 싶어",
    "시랑해": "사랑해",
    "사랑헤": "사랑해",
    "사라해": "사랑해",
    "머해": "뭐해",
    "모해": "뭐해",
    "뭐햐": "뭐해",
    "뭐하냐": "뭐해",
    "뭐함": "뭐해",
    "조아해": "좋아해",
    "조아": "좋아",
    "구래": "그래",
    "모르겟어": "모르겠어",
    "몰겟어": "모르겠어",
    "모르갰어": "모르겠어",
    "되써": "됐어",
    "대써": "됐어",
    "안녀": "안녕",
    "안뇽": "안녕",
    "안냥": "안녕",
    "고마어": "고마워",
    "고마워어": "고마워",
    "ㄱㅅ": "고마워",
    "기여워": "귀여워",
    "귀여어": "귀여워",
}


def _load_data():
    TYPING_DNA_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not TYPING_DNA_PATH.exists():
        data = {"counts": {}, "learned_patterns": {}, "meta": {"version": 1}}
        TYPING_DNA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return data
    try:
        data = json.loads(TYPING_DNA_PATH.read_text(encoding="utf-8"))
    except Exception:
        data = {"counts": {}, "learned_patterns": {}, "meta": {"version": 1}}
    if not isinstance(data, dict):
        data = {"counts": {}, "learned_patterns": {}, "meta": {"version": 1}}
    data.setdefault("counts", {})
    data.setdefault("learned_patterns", {})
    data.setdefault("meta", {"version": 1})
    return data


def _save_data(data):
    TYPING_DNA_PATH.parent.mkdir(parents=True, exist_ok=True)
    TYPING_DNA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _compact(text):
    return str(text or "").replace(" ", "").strip().lower()


def _replace_known_patterns(text):
    changed = False
    reasons = []
    normalized = text
    patterns = dict(TYPING_PATTERNS)
    patterns.update(_load_data().get("learned_patterns", {}))
    for typo, fixed in sorted(patterns.items(), key=lambda item: len(item[0]), reverse=True):
        if typo in normalized:
            normalized = normalized.replace(typo, fixed)
            changed = True
            reasons.append(f"{typo}->{fixed}")
            _record_seen(typo, fixed)
    return normalized, changed, reasons


def _keyboard_correction(text):
    compact = _compact(text)
    if any(_compact(word) in compact for word in SAFE_O_WORDS):
        return text, False, []

    corrected = KEYBOARD_H_CORRECTIONS.get(compact)
    if corrected:
        return corrected, True, [f"{compact}->{corrected}"]

    if compact.endswith("ㅗ"):
        base = compact[:-1]
        if base in ("웅", "응", "엉", "어", "아", "그래", "구래", "네", "넹", "넵", "안녕", "하이", "ㅇㅇ"):
            return base + "ㅎ", True, [f"{compact}->{base + 'ㅎ'}"]

    return text, False, []


def _record_seen(raw, normalized):
    if not raw or raw == normalized:
        return
    data = _load_data()
    key = f"{raw}=>{normalized}"
    data["counts"][key] = int(data["counts"].get(key, 0)) + 1
    if data["counts"][key] >= 3:
        data["learned_patterns"][raw] = normalized
    _save_data(data)


def record_typing_pattern(raw, normalized):
    _record_seen(str(raw or "").strip().lower(), str(normalized or "").strip().lower())
    return get_dictionary()


def get_dictionary():
    data = _load_data()
    dictionary = dict(TYPING_PATTERNS)
    dictionary.update(data.get("learned_patterns", {}))
    return dictionary


def normalize_for_analysis(message):
    info = analyze(message)
    return info["normalized_text"]


def analyze(message):
    original = str(message or "")
    normalized = original.lower().strip()
    changed = False
    reasons = []

    keyboard_text, keyboard_changed, keyboard_reasons = _keyboard_correction(normalized)
    if keyboard_changed:
        normalized = keyboard_text
        changed = True
        reasons.extend(keyboard_reasons)

    normalized, pattern_changed, pattern_reasons = _replace_known_patterns(normalized)
    if pattern_changed:
        changed = True
        reasons.extend(pattern_reasons)

    compact = _compact(normalized)
    affection = any(_compact(word) in compact for word in AFFECTION_WORDS)

    return {
        "original_text": original,
        "normalized_text": normalized,
        "changed": changed,
        "reasons": reasons,
        "affection_priority": affection,
    }
