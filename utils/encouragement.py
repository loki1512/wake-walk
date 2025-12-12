# utils/encouragement.py

import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_encouragement(
    *,
    woke_up: bool,
    walk_minutes: int | None,
    current_streak: int
) -> str:
    """
    Generates a high-energy encouragement message using Gemini.
    Falls back safely if Gemini fails.
    """

    # ---- Fallback (no Gemini) ----
    if not GEMINI_API_KEY:
        return (
            "LET’S GO! 💥 You showed up today — that’s how streaks are built. "
            "Keep the momentum rolling! 🚀"
        )

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-flash-latest")

        # ---- Build dynamic context ----
        walk_text = (
            f"{walk_minutes} minutes of walking"
            if walk_minutes and walk_minutes > 0
            else "no walk recorded yet"
        )

        wake_text = (
            "woke up and logged it"
            if woke_up
            else "did not log wake-up"
        )

        prompt = f"""
You are an energetic, motivating habit coach.
Your tone is upbeat, positive, and action-oriented.
Use emojis sparingly (1–2 max).
Keep it under 3 lines.

Today's stats:
- User {wake_text}
- User logged {walk_text}
- Current streak: {current_streak} days

Write a powerful encouragement message that makes the user feel proud and fired up.
"""

        response = model.generate_content(prompt)

        if response and response.text:
            return response.text.strip()

    except Exception as e:
        print("Gemini error:", e)

    # ---- Final fallback ----
    return (
        "🔥 BOOM! Another day, another step forward. "
        "You’re building something real — keep pushing! 💪"
    )
