# utils/emailer.py

import os
import smtplib
from email.message import EmailMessage
DISABLE_EMAIL = os.getenv("DISABLE_EMAIL") == "true"

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER)

def send_email(to_email: str, subject: str, body: str):
    if DISABLE_EMAIL:
        print("📧 Email disabled (Render free tier)")
        return
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS, to_email]):
        print("Email not sent: missing SMTP config")
        return

    msg = EmailMessage()
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
    except Exception as e:
        print("Email error:", e)
