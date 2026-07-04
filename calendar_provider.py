from datetime import date, datetime, timedelta
from pathlib import Path
import json
import uuid


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_SCHEDULE_PATH = BASE_DIR / "data" / "life_schedule.json"


class CalendarProvider:
    def sync_external_calendar(self):
        return {"status": "local_only", "message": "External calendar sync is not connected yet."}

    def get_today_events(self):
        return []

    def get_tomorrow_events(self):
        return []

    def get_week_events(self):
        return []

    def add_event(self, event):
        return None

    def delete_event(self, event_id):
        return False

    def update_event(self, event_id, updates):
        return None

    def search_events(self, keyword=None, event_type=None, date_from=None, date_to=None):
        return []


class LocalScheduleProvider(CalendarProvider):
    def __init__(self, path=None):
        self.path = Path(path) if path else DEFAULT_SCHEDULE_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text(
                json.dumps({"events": [], "meta": {"version": 1}}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    def _load(self):
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            data = {"events": [], "meta": {"version": 1}}
        if not isinstance(data, dict):
            data = {"events": [], "meta": {"version": 1}}
        data.setdefault("events", [])
        data.setdefault("meta", {"version": 1})
        return data

    def _save(self, data):
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _events(self):
        return list(self._load().get("events", []))

    def _between(self, event, start, end):
        event_date = str(event.get("date", ""))
        return str(start) <= event_date <= str(end)

    def get_today_events(self):
        today = date.today().isoformat()
        return self.search_events(date_from=today, date_to=today)

    def get_tomorrow_events(self):
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        return self.search_events(date_from=tomorrow, date_to=tomorrow)

    def get_week_events(self):
        start = date.today().isoformat()
        end = (date.today() + timedelta(days=7)).isoformat()
        return self.search_events(date_from=start, date_to=end)

    def add_event(self, event):
        data = self._load()
        new_event = dict(event or {})
        now = datetime.now().isoformat(timespec="seconds")
        new_event.setdefault("id", uuid.uuid4().hex[:12])
        new_event.setdefault("created_at", now)
        new_event["updated_at"] = now
        new_event.setdefault("completed", False)
        new_event.setdefault("source", "local")
        data["events"].append(new_event)
        self._save(data)
        return new_event

    def delete_event(self, event_id):
        data = self._load()
        before = len(data["events"])
        data["events"] = [event for event in data["events"] if event.get("id") != event_id]
        changed = len(data["events"]) != before
        if changed:
            self._save(data)
        return changed

    def update_event(self, event_id, updates):
        data = self._load()
        now = datetime.now().isoformat(timespec="seconds")
        for event in data["events"]:
            if event.get("id") == event_id:
                event.update(dict(updates or {}))
                event["updated_at"] = now
                self._save(data)
                return event
        return None

    def search_events(self, keyword=None, event_type=None, date_from=None, date_to=None):
        keyword_text = str(keyword or "").strip().lower()
        event_type_text = str(event_type or "").strip().lower()
        start = str(date_from or "0000-00-00")
        end = str(date_to or "9999-99-99")
        results = []
        for event in self._events():
            if event_type_text and str(event.get("type", "")).lower() != event_type_text:
                continue
            if not self._between(event, start, end):
                continue
            if keyword_text:
                haystack = " ".join(
                    str(event.get(key, "")) for key in ("title", "type", "original_text", "notes")
                ).lower()
                if keyword_text not in haystack:
                    continue
            results.append(event)
        return sorted(results, key=lambda item: (str(item.get("date", "")), str(item.get("time", ""))))


class ExternalCalendarProvider(CalendarProvider):
    def sync_external_calendar(self):
        return {
            "status": "placeholder",
            "providers": ["Google Calendar", "Windows Calendar", "Apple Calendar"],
        }

    def get_today_events(self):
        return []

    def get_tomorrow_events(self):
        return []

    def get_week_events(self):
        return []

    def add_event(self, event):
        return None

    def delete_event(self, event_id):
        return False

    def update_event(self, event_id, updates):
        return None

    def search_events(self, keyword=None, event_type=None, date_from=None, date_to=None):
        return []
