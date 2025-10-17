from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.intents import classify
from app import db
from app.formatters import fmt_score, fmt_match_line, fmt_scorers_list
from pathlib import Path
from fastapi.responses import HTMLResponse
from app import ai
from typing import List

app = FastAPI(title="SportSnap (Dummy Data)")

class AskIn(BaseModel):
    question: str

class ChatIn(BaseModel):
    message: str

class FlashcardOut(BaseModel):
    question: str
    answer: str

@app.get("/", response_class=HTMLResponse)
def home():
    index = (Path(__file__).resolve().parents[1] / "web" / "index.html").read_text(encoding="utf-8")
    return HTMLResponse(index)

@app.post("/ask")
def ask(payload: AskIn):
    intent, slots = classify(payload.question)
    conn = db.get_conn()
    try:
        if intent == "score_match":
            a, b = slots.get("a",""), slots.get("b","")
            m = db.find_match(conn, a, b)
            if not m: return {"answer":"I couldn't find that match in the dummy data."}
            return {"answer": fmt_score(m[6], m[7], m[8], m[9])}

        if intent == "who_scored_team":
            team = slots.get("team","")
            rows = db.find_team_goals(conn, team)
            if not rows: return {"answer": "No scorers for that team in the dummy data."}
            pretty = [f"{d} — {t} vs {opp} ({minute}' {scorer})" for minute, scorer, t, opp, d in rows]
            return {"answer": " ; ".join(pretty)}

        if intent == "stadium_match":
            a, b = slots.get("a",""), slots.get("b","")
            m = db.find_match(conn, a, b)
            if not m: return {"answer":"Not in dummy data."}
            return {"answer": f"{m[4]}, {m[5]}"}

        if intent == "sport_match":
            a, b = slots.get("a",""), slots.get("b","")
            m = db.find_match(conn, a, b)
            if not m: return {"answer":"Not in dummy data."}
            return {"answer": m[1]}

        if intent == "who_won_match":
            a, b = slots.get("a",""), slots.get("b","")
            m = db.find_match(conn, a, b)
            if not m: return {"answer":"Not in dummy data."}
            if m[8] == m[9]: return {"answer":"It was a draw."}
            winner = m[6] if m[8] > m[9] else m[7]
            return {"answer": f"{winner} won. Final: {fmt_score(m[6], m[7], m[8], m[9])}"}

        if intent == "tournament_match":
            a, b = slots.get("a",""), slots.get("b","")
            m = db.find_match(conn, a, b)
            if not m: return {"answer":"Not in dummy data."}
            return {"answer": m[2] or "No tournament recorded."}

        if intent == "datetime_match":
            a, b = slots.get("a",""), slots.get("b","")
            m = db.find_match(conn, a, b)
            if not m: return {"answer":"Not in dummy data."}
            return {"answer": m[3]}

        if intent == "list_scorers_match":
            a, b = slots.get("a",""), slots.get("b","")
            m = db.find_match(conn, a, b)
            if not m: return {"answer":"Not in dummy data."}
            rows = db.list_match_scorers(conn, m[0])
            return {"answer": fmt_scorers_list(rows)}

        if intent == "matches_today":
            rows = db.matches_today(conn)
            if not rows: return {"answer":"No matches today in the dummy data."}
            return {"answer": " | ".join([f"{r[1]} vs {r[2]} at {r[4]}, {r[5]} [{r[3]}]" for r in rows])}

        if intent == "matches_by_stadium":
            stadium = slots.get("stadium","")
            rows = db.matches_by_stadium(conn, stadium)
            if not rows: return {"answer":"No matches for that stadium in the dummy data."}
            return {"answer": " | ".join([f"{r[1]} vs {r[2]} [{r[3]}]" for r in rows])}

        return {
            "answer": "Sorry, I handle 10 question types only. Try examples like: "
                      "'score of Berlin FC vs Munich United', 'who scored for Berlin FC', "
                      "'where was Berlin FC vs Munich United'."
        }
    finally:
        conn.close()


@app.post("/chat")
def chat(payload: ChatIn):
    """AI-powered chat. Falls back to rule-based `ask` if AI not available."""
    # First try AI
    ai_resp = ai.ask_openai(payload.message)
    if ai_resp:
        return {"answer": ai_resp}
    # Fallback to rule-based classifier
    intent, slots = classify(payload.message)
    # reuse ask logic by wrapping into AskIn
    return ask(AskIn(question=payload.message))


@app.get("/flashcards", response_model=List[FlashcardOut])
def flashcards(limit: int = 5):
    """Return a small list of flashcards generated from the DB or AI."""
    conn = db.get_conn()
    try:
        # Try to generate via AI using a prompt that asks for flashcards
        prompt = (
            "Create %d short sports trivia flashcards (question | answer) from the following database of matches. "
            "Keep both question and answer concise.\n\n" % limit
        )
        ai_resp = ai.ask_openai(prompt)
        if ai_resp:
            cards = []
            for line in ai_resp.splitlines():
                if '|' in line:
                    q,a = [p.strip() for p in line.split('|',1)]
                    cards.append({"question": q, "answer": a})
                    if len(cards) >= limit: break
            if cards:
                return cards

        # Fallback: build from recent matches
        cur = conn.cursor()
        cur.execute("SELECT home_team, away_team, date, stadium FROM matches ORDER BY date DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        out = []
        for r in rows:
            q = f"Who played {r[0]} vs {r[1]} on {r[2]}?"
            a = f"{r[0]} vs {r[1]} at {r[3]} on {r[2]}"
            out.append({"question": q, "answer": a})
        return out
    finally:
        conn.close()
