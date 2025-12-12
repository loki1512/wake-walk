from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from models import Entry

USER_TZ = ZoneInfo("Asia/Kolkata")
WAKE_START = datetime.strptime("06:00", "%H:%M").time()
WAKE_END   = datetime.strptime("06:30", "%H:%M").time()

def wake_qualifies(wake):
    if not wake:
        return False
    dt = datetime.fromisoformat(wake)
    dt = dt.astimezone(USER_TZ)
    return WAKE_START <= dt.time() <= WAKE_END


def get_streak(user_id):
    today = datetime.now(USER_TZ).date()
    entries = Entry.query.filter(
        Entry.user_id == user_id
    ).order_by(Entry.entry_date.asc()).all()

    best = 0
    current = 0
    last_date = None

    for e in entries:
        qualifies = wake_qualifies(e.wake_time)
        if qualifies:
            if last_date and (e.entry_date - last_date).days == 1:
                current += 1
            else:
                current = 1
            last_date = e.entry_date
            best = max(best, current)
        else:
            last_date = e.entry_date
            current = 0

    # current streak from today backward
    cur = 0
    for i in range(365):
        d = today - timedelta(days=i)
        e = next((x for x in entries if x.entry_date == d), None)
        if e and wake_qualifies(e.wake_time):
            cur += 1
        else:
            break

    return {"current": cur, "best": best}
