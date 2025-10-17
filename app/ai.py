import os
from typing import Optional

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

def is_available() -> bool:
    return bool(OPENAI_KEY)

def ask_openai(prompt: str) -> Optional[str]:
    """Try to ask OpenAI (if API key present). Return text or None if not available."""
    if not is_available():
        return None
    try:
        import openai
        openai.api_key = OPENAI_KEY
        resp = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=256,
            temperature=0.7,
        )
        return resp.choices[0].text.strip()
    except Exception:
        return None
