from typing import List, Tuple, Optional

def fmt_score(home, away, hs, as_):
    return f"{home} {hs} – {as_} {away}"

def fmt_match_line(m):
    # matches columns:
    # id, sport, tournament, date, stadium, city, home_team, away_team, home_score, away_score
    return f"[{m[3]}] {m[6]} vs {m[7]} — {m[1]} at {m[4]}, {m[5]} (Tournament: {m[2]})"

def fmt_scorers_list(rows: List[Tuple[int,str,str]]):
    if not rows: return "No goal scorers recorded in the dummy data."
    parts = [f"{minute}' {team}: {name}" for minute, team, name in rows]
    return "Scorers: " + "; ".join(parts)
