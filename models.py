from datetime import datetime, date
from zoneinfo import ZoneInfo
from database import db
import bcrypt

USER_TZ = ZoneInfo("Asia/Kolkata")

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(USER_TZ))

    def set_password(self, pw):
        self.password_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

    def check_password(self, pw):
        return bcrypt.checkpw(pw.encode(), self.password_hash.encode())


class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    entry_date = db.Column(db.Date, nullable=False)
    wake_time = db.Column(db.String)
    walk_minutes = db.Column(db.Integer)
    note = db.Column(db.Text)

    user = db.relationship("User", backref="entries")
