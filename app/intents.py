import re
from typing import Dict, Optional, Tuple

# Define 10 intents
INTENT_PATTERNS = [
    ("score_match", re.compile(r"(score|result).+?(?P<a>.+?)\s+(vs|v|against)\s+(?P<b>.+)", re.I)),
    ("who_scored_team", re.compile(r"who\s+scored\s+for\s+(?P<team>.+)", re.I)),
    ("stadium_match", re.compile(r"(where|stadium|location).+?(?P<a>.+?)\s+(vs|v|against)\s+(?P<b>.+)", re.I)),
    ("sport_match", re.compile(r"(what\s+sport).+?(?P<a>.+?)\s+(vs|v|against)\s+(?P<b>.+)", re.I)),
    ("who_won_match", re.compile(r"(who\s+won).+?(?P<a>.+?)\s+(vs|v|against)\s+(?P<b>.+)", re.I)),
    ("tournament_match", re.compile(r"(tournament|competition).+?(?P<a>.+?)\s+(vs|v|against)\s+(?P<b>.+)", re.I)),
    ("datetime_match", re.compile(r"(when|date|time).+?(?P<a>.+?)\s+(vs|v|against)\s+(?P<b>.+)", re.I)),
    ("list_scorers_match", re.compile(r"(list|show).+?(scorers|goal\s*scorers).+?(?P<a>.+?)\s+(vs|v|against)\s+(?P<b>.+)", re.I)),
    ("matches_today", re.compile(r"(matches|games)\s+(today|for\s+today)", re.I)),
    ("matches_by_stadium", re.compile(r"(matches|games).+?(at|in)\s+(?P<stadium>.+)", re.I)),
]

def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())

def classify(question: str) -> Tuple[str, Dict[str, str]]:
    q = question.strip()
    for name, pat in INTENT_PATTERNS:
        m = pat.search(q)
        if m:
            groups = {k: _clean(v) for k,v in m.groupdict().items() if v}
            return name, groups
    # Heuristic fallbacks
    if "score" in q.lower() and "vs" in q.lower():
        parts = re.split(r"vs|v|against", q, flags=re.I)
        if len(parts) >= 2:
            return "score_match", {"a": _clean(parts[0].split()[-1]), "b": _clean(parts[1])}
    return "unknown", {}
