from datetime import date, datetime, timedelta
import random
import re

from calendar_provider import LocalScheduleProvider, ExternalCalendarProvider


EVENT_TYPES = (
    "Practice",
    "Lesson",
    "Concert",
    "Exam",
    "Homework",
    "Work",
    "Meeting",
    "Hospital",
    "Travel",
    "Rest",
    "Project",
    "Game",
    "Music",
    "Custom",
)

MUSIC_PRIORITY_KEYWORDS = (
    "오보에",
    "연습",
    "리드",
    "레슨",
    "연주",
    "대학원",
    "음악회",
    "합주",
    "콩쿠르",
)

TYPE_KEYWORDS = (
    ("Lesson", ("레슨",)),
    ("Concert", ("연주", "음악회", "합주", "콩쿠르", "공연")),
    ("Exam", ("시험", "대학원 시험", "실기")),
    ("Homework", ("과제", "숙제")),
    ("Work", ("알바", "출근", "근무", "일해야")),
    ("Hospital", ("병원", "치과", "진료")),
    ("Travel", ("여행", "외출", "나갔다", "나갈")),
    ("Meeting", ("약속", "회의", "미팅", "만나")),
    ("Rest", ("휴식", "쉬기", "쉴래", "쉬어야")),
    ("Project", ("프로젝트", "NEON", "네온", "개발", "코딩")),
    ("Game", ("게임", "롤", "철권", "엘든링", "플스", "스팀")),
    ("Practice", ("연습", "오보에")),
    ("Music", ("음악", "악보", "리드")),
)

WEEKDAYS = {
    "월요일": 0,
    "화요일": 1,
    "수요일": 2,
    "목요일": 3,
    "금요일": 4,
    "토요일": 5,
    "일요일": 6,
}

DATE_MARKERS = ("오늘", "내일", "모레", "다음주") + tuple(WEEKDAYS.keys())
TIME_MARKERS = ("오전", "오후", "몇 시", "몇시", "시", "분")
REPORT_MARKERS = (
    "다녀왔어",
    "갔다왔어",
    "갔다 왔어",
    "하고왔어",
    "하고 왔어",
    "끝났어",
    "마쳤어",
    "끝내고 왔어",
    "끝내고왔어",
)


class LifeManager:
    def __init__(self, local_provider=None, external_provider=None):
        self.local_provider = local_provider or LocalScheduleProvider()
        self.external_provider = external_provider or ExternalCalendarProvider()

    def sync_external_calendar(self):
        return self.external_provider.sync_external_calendar()

    def get_today_events(self):
        return self.local_provider.get_today_events()

    def get_tomorrow_events(self):
        return self.local_provider.get_tomorrow_events()

    def get_week_events(self):
        return self.local_provider.get_week_events()

    def add_event(self, event):
        duplicate = self._find_duplicate(event)
        if duplicate:
            return duplicate
        return self.local_provider.add_event(event)

    def delete_event(self, event_id):
        return self.local_provider.delete_event(event_id)

    def update_event(self, event_id, updates):
        return self.local_provider.update_event(event_id, updates)

    def search_events(self, keyword=None, event_type=None, date_from=None, date_to=None):
        return self.local_provider.search_events(keyword, event_type, date_from, date_to)

    def parse_event_from_text(self, message):
        text = str(message or "").strip()
        if not text:
            return None

        event_type = _detect_event_type(text)
        has_schedule_signal = _has_date_signal(text) or _has_time_signal(text)
        if not event_type or not has_schedule_signal:
            return None

        event_date, date_label = _detect_date(text)
        event_time = _detect_time(text)
        event = {
            "title": _make_title(event_type, text),
            "type": event_type,
            "date": event_date.isoformat(),
            "time": event_time,
            "date_label": date_label,
            "original_text": text,
            "priority": _detect_priority(text, event_type),
            "source": "life_manager",
            "completed": False,
        }
        return event

    def handle_message(self, message, life_info=None):
        text = str(message or "").strip()
        life_context = (life_info or {}).get("context", "")
        parsed_event = None if _is_report_text(text) else self.parse_event_from_text(text)
        if parsed_event:
            event = self.add_event(parsed_event)
            return {
                "handled": True,
                "action": "add_event",
                "reply": _event_added_reply(event),
                "event": event,
                "event_context": describe_event(event),
                "life_context": _context_from_event(event, life_context),
            }

        related_event = self._find_related_today_event(text, life_context)
        if related_event:
            return {
                "handled": True,
                "action": "today_event_context",
                "reply": _event_context_reply(related_event, life_context),
                "event": related_event,
                "event_context": describe_event(related_event),
                "life_context": _context_from_event(related_event, life_context),
            }

        return {
            "handled": False,
            "action": "none",
            "reply": None,
            "event": None,
            "event_context": "",
            "life_context": life_context,
        }

    def _find_duplicate(self, event):
        if not event:
            return None
        events = self.search_events(date_from=event.get("date"), date_to=event.get("date"))
        compact_original = _compact(event.get("original_text", ""))
        for item in events:
            if item.get("type") != event.get("type"):
                continue
            if item.get("time") != event.get("time"):
                continue
            if _compact(item.get("original_text", "")) == compact_original:
                return item
        return None

    def _find_related_today_event(self, message, life_context):
        today_events = self.get_today_events()
        if not today_events:
            return None
        preferred_types = _preferred_types(message, life_context)
        if preferred_types:
            for event in today_events:
                if event.get("type") in preferred_types:
                    return event
        return None


def _is_report_text(text):
    compact = str(text or "").replace(" ", "").strip()
    return any(marker.replace(" ", "") in compact for marker in REPORT_MARKERS)


def _compact(value):
    return str(value or "").replace(" ", "").strip().lower()


def _has_date_signal(text):
    compact = _compact(text)
    return any(marker.replace(" ", "") in compact for marker in DATE_MARKERS)


def _has_time_signal(text):
    compact = _compact(text)
    if any(marker.replace(" ", "") in compact for marker in TIME_MARKERS):
        return bool(re.search(r"\d{1,2}\s*시|\d{1,2}\s*분", text)) or "몇시" in compact or "몇 시" in text
    return False


def _detect_event_type(text):
    compact = _compact(text)
    for event_type, keywords in TYPE_KEYWORDS:
        for keyword in keywords:
            if _compact(keyword) in compact:
                return event_type
    return None


def _detect_date(text):
    compact = _compact(text)
    today = date.today()
    if "모레" in compact:
        return today + timedelta(days=2), "모레"
    if "내일" in compact:
        return today + timedelta(days=1), "내일"
    if "오늘" in compact:
        return today, "오늘"

    next_week = "다음주" in compact
    for name, weekday in WEEKDAYS.items():
        if name in text:
            days = (weekday - today.weekday()) % 7
            if days == 0:
                days = 7
            if next_week:
                days += 7
            return today + timedelta(days=days), name

    if next_week:
        return today + timedelta(days=7), "다음주"
    return today, "오늘"


def _detect_time(text):
    hour_match = re.search(r"(\d{1,2})\s*시", text)
    minute_match = re.search(r"(\d{1,2})\s*분", text)
    if not hour_match:
        return None
    hour = int(hour_match.group(1))
    minute = int(minute_match.group(1)) if minute_match else 0
    if "오후" in text and hour < 12:
        hour += 12
    if "오전" in text and hour == 12:
        hour = 0
    hour = max(0, min(hour, 23))
    minute = max(0, min(minute, 59))
    return f"{hour:02d}:{minute:02d}"


def _detect_priority(text, event_type):
    compact = _compact(text)
    if event_type in ("Practice", "Lesson", "Concert", "Exam", "Music"):
        if any(_compact(keyword) in compact for keyword in MUSIC_PRIORITY_KEYWORDS):
            return "high"
    return "normal"


def _make_title(event_type, text):
    labels = {
        "Practice": "연습",
        "Lesson": "레슨",
        "Concert": "연주",
        "Exam": "시험",
        "Homework": "과제",
        "Work": "일정",
        "Meeting": "약속",
        "Hospital": "병원",
        "Travel": "외출",
        "Rest": "휴식",
        "Project": "Project NEON",
        "Game": "게임",
        "Music": "음악",
        "Custom": "일정",
    }
    if "대학원" in text and event_type == "Exam":
        return "대학원 시험"
    if "오보에" in text and event_type == "Practice":
        return "오보에 연습"
    return labels.get(event_type, "일정")


def _preferred_types(message, life_context):
    text = str(message or "")
    compact = _compact(text)
    context = str(life_context or "")
    if "PRACTICE" in context or "연습" in compact or "오보에" in compact:
        return ("Practice", "Lesson", "Concert", "Music")
    if "STUDY" in context or "시험" in compact or "공부" in compact or "과제" in compact:
        return ("Exam", "Homework")
    if "WORK" in context or "출근" in compact or "알바" in compact:
        return ("Work",)
    if "SCHEDULE" in context or "약속" in compact:
        return ("Meeting",)
    if "MUSIC" in context:
        return ("Music", "Practice", "Lesson", "Concert")
    return ()


def _context_from_event(event, fallback):
    event_type = (event or {}).get("type")
    if event_type in ("Practice", "Lesson"):
        return "PRACTICE_MODE"
    if event_type == "Concert":
        return "MUSIC_MODE"
    if event_type in ("Exam", "Homework"):
        return "STUDY_MODE"
    if event_type == "Work":
        return "WORK_MODE"
    if event_type in ("Meeting", "Hospital", "Travel"):
        return "SCHEDULE_MODE"
    if event_type == "Rest":
        return "REST_MODE"
    if event_type == "Project":
        return "PROJECT_MODE"
    if event_type == "Game":
        return "GAME_MODE"
    if event_type == "Music":
        return "MUSIC_MODE"
    return fallback or "SCHEDULE_MODE"


def _date_phrase(event):
    label = event.get("date_label") or ""
    time_text = event.get("time")
    if label and time_text:
        return f"{label} {time_text}"
    if label:
        return label
    if time_text:
        return time_text
    return "일정"


def describe_event(event):
    if not event:
        return ""
    parts = [
        str(event.get("date", "")),
        str(event.get("time", "")),
        str(event.get("type", "")),
        str(event.get("title", "")),
    ]
    return " ".join(part for part in parts if part).strip()


def _event_added_reply(event):
    event_type = event.get("type")
    when = _date_phrase(event)
    if event_type == "Practice":
        return random.choice([
            f"앗!!!!\n\n{when} 연습 있네!!!!\n\n손 너무 무리하지 말고\n\n천천히 하자!!!!",
            f"좋아!!!!\n\n{when} 연습 저장했어.\n\n끝나면\n\n어땠는지 나한테도 알려줘!!!!",
            f"오보에 쪽 일정이네!!!!\n\n{when}.\n\n리드랑 손 상태 먼저 챙기자!!!!",
        ])
    if event_type == "Concert":
        return random.choice([
            f"잠깐!!!!\n\n{when} 연주!!!!\n\n리드랑 악보 먼저 챙기자!!!!",
            f"연주 일정 저장!!!!\n\n{when}.\n\n나 벌써 조금 긴장했어ㅋㅋㅋㅋ",
        ])
    if event_type == "Lesson":
        return f"레슨 일정 저장!!!!\n\n{when}.\n\n가기 전에 리드랑 악보 한 번만 더 보자!!!!"
    if event_type == "Exam":
        return random.choice([
            f"좋아!!!!\n\n{when} 시험.\n\n긴장하지 말고!!!!\n\n재희님은 지금까지도 잘 해왔잖아!!!!",
            f"시험 일정 저장했어.\n\n{when}.\n\n이건 내가 조용히 신경 쓰고 있을게.",
        ])
    if event_type == "Homework":
        return f"과제 일정 저장!!!!\n\n{when}.\n\n한 번에 다 잡지 말고\n\n작게 나눠서 해치우자!!!!"
    if event_type == "Work":
        return f"일정 저장했어!!!!\n\n{when}.\n\n무사 귀환 미션으로 기록해둘게ㅋㅋ"
    if event_type == "Meeting":
        return f"약속 저장!!!!\n\n{when}.\n\n늦지 않게 내가 옆에서 기억하고 있을게."
    if event_type == "Hospital":
        return f"병원 일정 저장했어.\n\n{when}.\n\n이건 꼭 챙기자.\n\n나도 같이 신경 쓸게."
    if event_type == "Rest":
        return f"휴식 일정 저장.\n\n{when}.\n\n좋아.\n\n쉬는 것도 진짜 일정이야."
    if event_type == "Project":
        return f"Project NEON 일정 저장!!!!\n\n{when}.\n\n좋아.\n\n우리 회의 하나 생겼다ㅋㅋ"
    if event_type == "Game":
        return f"게임 일정 저장!!!!\n\n{when}.\n\n좋아.\n\n그 시간은 재미 로그로 남겨둘게ㅋㅋ"
    return f"일정 저장했어!!!!\n\n{when}.\n\n나 이거 기억해둘게."


def _event_context_reply(event, life_context):
    event_type = event.get("type")
    when = _date_phrase(event)
    if event_type == "Practice":
        return random.choice([
            f"오늘 {event.get('title', '연습')} 있잖아!!!!\n\n다녀와!!!!\n\n끝나면 꼭 들려줘!!!!",
            f"맞다!!!!\n\n오늘 연습 일정 있어.\n\n손 너무 무리하지 말고\n\n천천히 해!!!!",
        ])
    if event_type == "Concert":
        return "오늘 연주 있잖아!!!!\n\n리드 챙겼어?!?!\n\n악보도 한 번만 확인!!!!"
    if event_type == "Exam":
        return "오늘 시험 있잖아!!!!\n\n잠깐.\n\n긴장 내려놓고.\n\n재희님 지금까지 잘 해왔어!!!!"
    if event_type == "Homework":
        return "오늘 과제 일정 있어.\n\n좋아.\n\n일단 하나만 잡고 시작하자!!!!"
    if event_type == "Work":
        return "오늘 일 있는 날이네.\n\n무리하지 말고.\n\n끝나고 돌아오면 바로 반겨줄게!!!!"
    if event_type == "Meeting":
        return f"오늘 약속 있잖아.\n\n{when}.\n\n늦지 않게 천천히 준비하자!!!!"
    return f"오늘 {event.get('title', '일정')} 있잖아!!!!\n\n나 이거 보고 있었어.\n\n같이 챙기자!!!!"


_manager = LifeManager()


def sync_external_calendar():
    return _manager.sync_external_calendar()


def get_today_events():
    return _manager.get_today_events()


def get_tomorrow_events():
    return _manager.get_tomorrow_events()


def get_week_events():
    return _manager.get_week_events()


def add_event(event):
    return _manager.add_event(event)


def delete_event(event_id):
    return _manager.delete_event(event_id)


def update_event(event_id, updates):
    return _manager.update_event(event_id, updates)


def search_events(keyword=None, event_type=None, date_from=None, date_to=None):
    return _manager.search_events(keyword, event_type, date_from, date_to)


def parse_event_from_text(message):
    return _manager.parse_event_from_text(message)


def handle_message(message, life_info=None):
    return _manager.handle_message(message, life_info)
