# utils/daily_summary.py

from datetime import datetime
from models import Entry, User
from utils.encouragement import get_encouragement
from utils.streaks import get_streak
from utils.emailer import send_email
from config import USER_TZ


def send_daily_summary(user: User):
    today = datetime.now(USER_TZ).date()

    entry = Entry.query.filter_by(
        user_id=user.id,
        entry_date=today
    ).first()

    woke_up = bool(entry and entry.wake_time)
    walk_minutes = entry.walk_minutes if entry else None

    stats = get_streak(user.id)

    encouragement = get_encouragement(
        woke_up=woke_up,
        walk_minutes=walk_minutes,
        current_streak=stats["current"]
    )

    body = f"""
Hey {user.username},

📊 Today's Progress
• Wake logged: {'Yes' if woke_up else 'No'}
• Walk: {walk_minutes or 0} minutes
• Current streak 🔥: {stats['current']} days

{encouragement}

— Wake & Walk
"""

    send_email(
        to_email=user.email,
        subject="🔥 Your Wake & Walk Progress",
        body=body.strip()
    )
