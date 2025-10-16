import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "sportchat.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def find_match(conn, a: str, b: str):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM matches
        WHERE lower(home_team) LIKE lower(?) AND lower(away_team) LIKE lower(?)
        """,
        (f"%{a}%", f"%{b}%")
    )
    return cur.fetchone()

def find_team_goals(conn, team: str) -> list[tuple]:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT g.minute, g.scorer_name, m.home_team, m.away_team, m.date
        FROM goals g
        JOIN matches m ON m.id = g.match_id
        WHERE lower(g.team) LIKE lower(?)
        ORDER BY m.date, g.minute
        """,
        (f"%{team}%",)
    )
    return cur.fetchall()

def list_match_scorers(conn, match_id: int) -> list[tuple]:
    cur = conn.cursor()
    cur.execute("SELECT minute, team, scorer_name FROM goals WHERE match_id=? ORDER BY minute", (match_id,))
    return cur.fetchall()

def matches_today(conn) -> list[tuple]:
    cur = conn.cursor()
    cur.execute("SELECT id, home_team, away_team, date, stadium, city FROM matches WHERE date=date('now')")
    return cur.fetchall()

def matches_by_stadium(conn, stadium: str) -> list[tuple]:
    cur = conn.cursor()
    cur.execute("SELECT id, home_team, away_team, date, stadium, city FROM matches WHERE lower(stadium) LIKE lower(?)", (f"%{stadium}%",))
    return cur.fetchall()
