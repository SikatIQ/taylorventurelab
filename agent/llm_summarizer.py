import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env if present
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUMMARY_MODEL_NAME = os.getenv("SUMMARY_MODEL_NAME", "gpt-4o-mini")

_client: Optional[OpenAI] = None


def get_client() -> OpenAI:
    """
    Lazily initialize the OpenAI client.
    """
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set in environment.")
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def summarize_article(
    article_text: str,
    label: str = "General Marketing",
    max_tokens: int = 400,
    temperature: float = 0.3,
) -> str:
    """
    Use OpenAI to summarize a full article into a short, punchy summary for
    a senior marketing / strategy audience.

    Returns a markdown-compatible string.
    """
    client = get_client()

    # Trim text if it's extremely long
    trimmed_text = article_text
    if len(trimmed_text) > 12000:
        trimmed_text = trimmed_text[:12000]

    system_msg = (
        "You are an expert marketing and strategy analyst. "
        "You write concise, insightful summaries that highlight why a piece "
        "of content matters for social media, growth, and strategic decision-making."
    )

    user_msg = (
        f"Topic label: {label}\n\n"
        "Summarize the following article in 3–5 bullet points for a senior marketing/strategy audience. "
        "Focus on key insights, actionable tactics, or strategic implications. "
        "Avoid fluff. Do not exceed 180 words.\n\n"
        "Article:\n"
        f"{trimmed_text}"
    )

    response = client.chat.completions.create(
        model=SUMMARY_MODEL_NAME,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )

    content = response.choices[0].message.content.strip()
    return content
