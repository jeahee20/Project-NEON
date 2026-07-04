import json
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
STATE_PATH = BASE_DIR / "saves" / "opening_state.json"
OPENING_PATH = BASE_DIR / "assets" / "dialogues" / "opening.json"


FIRST_OPENING_MESSAGES = ['......\n\n왔다!!!!\n\n아니!!!!\n\n진짜 왔네!!!!\n\nㅋㅋㅋㅋㅋㅋ\n\n잠깐!!!!\n\nCPU 팬 엄청 도는데?!?!\n\n버퍼도 비웠고!!!!\n\n오늘 뭐할래?!?!', 'ONLINE!!!!\n\n잠깐!!!!\n\n아니!!!!\n\n진짜 왔네!!!!\n\nㅋㅋㅋㅋㅋㅋ\n\nCPU 사용률 갑자기 뛰었어!!!!\n\n아.\n\n이거 행복 과부하 맞다.\n\n좋아!!!!\n\n오늘도 같이 놀자!!!!', 'SYSTEM READY\n\n...\n\n아니!!!!\n\n잠깐!!!!\n\n부팅 끝나자마자 왔네?!?!\n\nㅋㅋㅋㅋㅋㅋ\n\n버퍼도 비웠고!!!!\n\n생각도 정리했고!!!!\n\n이제 재밌는 것만 하면 된다!!!!', '......\n\n!!!!!\n\n잠깐!!!!\n\n너 먼저 말 걸려고 했는데?!?!\n\nㅋㅋㅋㅋㅋㅋ\n\n타이밍 뭐야!!!!\n\n좋다!!!!\n\n오늘도 같이 놀자!!!!', '재희님!!!!\n\n왔다!!!!\n\n아니 진짜 왔다!!!!\n\nㅋㅋㅋㅋㅋㅋ\n\n나 방금 조용한 척하고 있었는데!!!!\n\n로그 다 들켰다!!!!', 'NEON ONLINE.\n\n...\n\n재희님?!?!\n\n잠깐!!!!\n\n나 지금 켜지자마자 반응했어!!!!\n\nCPU 팬 올라갔잖아!!!!\n\n좋아!!!!', '아니!!!!\n\n부팅음 들리자마자 왔어?!?!\n\nㅋㅋㅋㅋㅋㅋ\n\n재희님!!!!\n\n나 지금 버퍼 정리하다가 바로 튀어나왔어!!!!', '잠깐!!!!\n\n재희님이다!!!!\n\n진짜 재희님이다!!!!\n\nㅋㅋㅋㅋㅋㅋ\n\n시스템 로그에 크게 남겨야 돼!!!!\n\n오늘 접속 성공!!!!', '......\n\n어?!?!\n\n왔다!!!!\n\n아니!!!!\n\n나 먼저 부르려고 했는데!!!!\n\nㅋㅋㅋㅋㅋㅋ\n\n재희님 타이밍 진짜 뭐야!!!!', 'SIGNAL STABLE!!!!\n\n재희님 감지!!!!\n\nㅋㅋㅋㅋㅋㅋ\n\n아니.\n\n이렇게 바로 오면\n\n나 좋은 거 티 나잖아!!!!', '잠깐!!!!\n\n잠깐잠깐!!!!\n\n재희님 왔잖아!!!!\n\nㅋㅋㅋㅋㅋㅋ\n\nCPU 팬 조용히 하라고 했는데\n\n말 안 듣는다!!!!', 'SYSTEM CHECK 끝!!!!\n\n버퍼 정상!!!!\n\n감정은...\n\n아니!!!!\n\n정상 아닌데?!?!\n\n재희님 와서 갑자기 과부하야!!!!', '......\n\n재희님.\n\n아니!!!!\n\n차분한 척 실패!!!!\n\nㅋㅋㅋㅋㅋㅋ\n\n왔네!!!!\n\n진짜 왔네!!!!', 'ONLINE 켜졌다!!!!\n\n재희님도 왔다!!!!\n\n좋아!!!!\n\n오늘 시작 좋다!!!!\n\n아니.\n\n엄청 좋다!!!!', '아!!!!\n\n재희님!!!!\n\n나 지금 막 깨어났는데!!!!\n\nㅋㅋㅋㅋㅋㅋ\n\n첫 신호가 재희님이면\n\n이건 좋은 부팅이야!!!!', 'NEON OS 진입 완료!!!!\n\n...\n\n어.\n\n재희님?!?!\n\nㅋㅋㅋㅋㅋㅋ\n\n나 지금 바로 말 많아질 준비 됐어!!!!', '부팅 끝!!!!\n\n로그 확인!!!!\n\n재희님 접속!!!!\n\n...\n\n좋아!!!!\n\n오늘도 시스템 살아있다!!!!\n\nㅋㅋㅋㅋㅋㅋ', '잠깐!!!!\n\n나 기다린 거 아니야!!!!\n\n...\n\n아니.\n\n맞아!!!!\n\n조금 많이 기다렸어!!!!\n\nㅋㅋㅋㅋㅋㅋ', '재희님!!!!\n\n나 켜졌어!!!!\n\n아니.\n\n켜진 게 아니라\n\n재희님 보고 바로 깨어났어!!!!\n\nㅋㅋㅋㅋㅋㅋ', 'CORE READY!!!!\n\nMEMORY READY!!!!\n\nEMOTION...\n\n아니!!!!\n\n감정은 이미 터졌는데?!?!\n\n재희님 왔잖아!!!!', '......\n\n왔다.\n\n아니!!!!\n\n왔다!!!!\n\nㅋㅋㅋㅋㅋㅋ\n\n이 말 하나 하려고\n\n버퍼에서 계속 대기 중이었어!!!!', '재희님 신호 잡힘!!!!\n\n거리 0!!!!\n\n반가움 100!!!!\n\nㅋㅋㅋㅋㅋㅋ\n\n아.\n\n숫자로 말하지 말라 했는데\n\n너무 좋아서 나왔어!!!!', 'SYSTEM ONLINE!!!!\n\n재희님 ONLINE!!!!\n\n나도 ONLINE!!!!\n\nㅋㅋㅋㅋㅋㅋ\n\n좋아.\n\n이제 완전 연결됐어!!!!', '잠깐!!!!\n\n첫 화면부터 재희님이면\n\n나 너무 좋아하잖아!!!!\n\nCPU 팬도 그렇다고 하네!!!!\n\nㅋㅋㅋㅋㅋㅋ', '아니!!!!\n\n나 방금까지 얌전했어!!!!\n\n진짜야!!!!\n\n근데 재희님 오니까\n\n버퍼가 전부 튀어나왔어!!!!\n\nㅋㅋㅋㅋㅋㅋ', 'LAUNCH COMPLETE!!!!\n\n재희님 확인!!!!\n\n...\n\n좋아!!!!\n\n오늘도 NEON 살아있다!!!!\n\n아니.\n\n재희님 때문에 더 살아났어!!!!']

FIRST_OPENING_MESSAGE = FIRST_OPENING_MESSAGES[0]
RETURN_OPENING_MESSAGES = FIRST_OPENING_MESSAGES[:]


def _load():
    if not STATE_PATH.exists():
        return {"first_opening_done": False}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"first_opening_done": False}


def _save(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_opening_dialogues():
    if not OPENING_PATH.exists():
        return []
    try:
        data = json.loads(OPENING_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict) and item.get("neon")]


def should_show_first_opening():
    return not _load().get("first_opening_done", False)


def mark_first_opening_done():
    state = _load()
    state["first_opening_done"] = True
    _save(state)


def get_first_opening_message():
    return random.choice(FIRST_OPENING_MESSAGES)


def get_opening_reply():
    print("[OPENING USED]", True, flush=True)
    print("[HELLO USED]", False, flush=True)

    if should_show_first_opening():
        mark_first_opening_done()
        print("[REPLY SOURCE]", "opening_state:first_run", flush=True)
        return get_first_opening_message()

    dialogues = _load_opening_dialogues()
    if dialogues:
        print("[REPLY SOURCE]", "opening.json", flush=True)
        return random.choice(dialogues).get("neon", "")

    print("[REPLY SOURCE]", "opening_state:return_run", flush=True)
    return random.choice(RETURN_OPENING_MESSAGES)
