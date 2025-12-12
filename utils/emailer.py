import smtplib
from email.message import EmailMessage
from config import Config

def send_email(to_email, subject, body):
    """
    Sends an email using SMTP credentials defined in environment or config.
    Returns True if successful, False otherwise.
    """

    if not Config.SMTP_HOST or not Config.SMTP_USER or not Config.SMTP_PASS:
        print("⚠️ SMTP not configured — skipping email.")
        return False

    msg = EmailMessage()
    msg["From"] = Config.EMAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT, timeout=10) as s:
            s.starttls()
            s.login(Config.SMTP_USER, Config.SMTP_PASS)
            s.send_message(msg)

        print(f"📨 Email sent to {to_email}")
        return True

    except Exception as e:
        print("❌ Failed to send email:", e)
        return False
