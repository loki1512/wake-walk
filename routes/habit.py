from flask import Blueprint, request, jsonify
from functools import wraps
import jwt
from datetime import datetime
from zoneinfo import ZoneInfo
from models import Entry
from config import Config
# from models import Entry
from utils.streaks import get_streak, wake_qualifies
from utils.encouragement import get_encouragement
from database import db

habit_bp = Blueprint("habit", __name__)
USER_TZ = ZoneInfo("Asia/Kolkata")


def require_jwt(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        try:
            data = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
            request.user_id = data["user_id"]
        except:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper


@habit_bp.route("/api/wakeup", methods=["POST"])
@require_jwt
def wakeup():
    before = get_streak(request.user_id)["current"]

    ts = datetime.now(USER_TZ).isoformat()
    today = datetime.now(USER_TZ).date()

    entry = Entry.query.filter_by(user_id=request.user_id, entry_date=today).first()
    if not entry:
        entry = Entry(user_id=request.user_id, entry_date=today)

    entry.wake_time = ts
    db.session.add(entry)
    db.session.commit()

    after = get_streak(request.user_id)["current"]
    increased = after > before

    return jsonify({"status": "ok", "streak_increased": increased})


# @habit_bp.route("/api/walk", methods=["POST"])
# @require_jwt
# def walk():
#     before = get_streak(request.user_id)["current"]

#     minutes = int((request.json or {}).get("minutes", 0))
#     today = datetime.now(USER_TZ).date()

#     entry = Entry.query.filter_by(user_id=request.user_id, entry_date=today).first()
#     if not entry:
#         entry = Entry(user_id=request.user_id, entry_date=today)

#     entry.walk_minutes = minutes
#     db.session.add(entry)
#     db.session.commit()

#     after = get_streak(request.user_id)["current"]
#     increased = after > before

#     return jsonify({"status": "ok", "streak_increased": increased})

@habit_bp.route("/api/stats", methods=["GET"])
@require_jwt
def stats():
    from utils.streaks import get_streak
    return get_streak(request.user_id)

@habit_bp.route("/recent", methods=["GET"])
@require_jwt
def recent_entries():
    from models import Entry

    entries = (
        Entry.query
        .filter_by(user_id=request.user_id)
        .order_by(Entry.entry_date.desc())
        .limit(30)
        .all()
    )

    result = []
    for e in entries:
        result.append({
            "entry_date": e.entry_date.isoformat(),
            "wake_time": e.wake_time,
            "walk_minutes": e.walk_minutes
        })

    return result
@habit_bp.route("/api/test-email", methods=["POST"])
@require_jwt
def test_email():
    from models import User
    from utils.daily_summary import send_daily_summary

    user = User.query.get(request.user_id)
    send_daily_summary(user)

    return {"status": "email sent (if configured)"}

@habit_bp.route("/api/walk", methods=["POST"])
@require_jwt
def record_walk():
    from datetime import datetime
    from models import Entry, User
    from utils.daily_summary import send_daily_summary
    from utils.streaks import get_streak

    data = request.get_json()
    minutes = data.get("minutes")

    if not minutes or minutes <= 0:
        return {"error": "Invalid minutes"}, 400

    today = datetime.now(USER_TZ).date()

    entry = Entry.query.filter_by(
        user_id=request.user_id,
        entry_date=today
    ).first()

    if not entry:
        entry = Entry(user_id=request.user_id, entry_date=today)

    entry.walk_minutes = minutes
    db.session.add(entry)
    db.session.commit()

    # 👉 TESTING ONLY: send email on walk
    try:
        user = User.query.get(request.user_id)
        send_daily_summary(user)
    except Exception as e:
        print("Email test failed:", e)

    stats = get_streak(request.user_id)

    return {
        "status": "ok",
        "streak_increased": stats["current"] > 0,
        "current_streak": stats["current"]
    }
