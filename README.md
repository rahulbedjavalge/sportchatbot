# SportSnap — Phase 2 (Implementation)

Lightweight sports-results chatbot using **dummy data**. Supports exactly **10 intents** with a tiny FastAPI backend and SQLite database.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/create_db.py             # creates sportchat.db from data/seed.sql
uvicorn app.main:app --reload           # http://127.0.0.1:8000
```

- Open `http://127.0.0.1:8000/` for a minimal chat UI.
- Or POST to `/ask` with: `{"question": "Who scored for Berlin FC?"}`

## Supported intents (10)
1. Score of <Team A> vs <Team B>
2. Who scored for <Team>
3. Stadium/location of <A> vs <B>
4. What sport was <A> vs <B>
5. Who won <A> vs <B>
6. Tournament of <A> vs <B>
7. Date/time of <A> vs <B>
8. List goal scorers in <A> vs <B>
9. Show all matches today
10. Show matches by stadium <Name>

## Project layout
```
sportchat/
  app/
    main.py         # API routes
    intents.py      # 10-intent matcher (regex/keywords)
    db.py           # SQLite helpers and queries
    formatters.py   # Answer text formatting
  data/
    seed.sql        # schema + dummy INSERTs
  scripts/
    create_db.py    # build sportchat.db from seed.sql
  tests/
    test_intents.py # smoke tests for the 10 intents
  web/
    index.html      # minimal chat web UI
  requirements.txt
  README.md
```

## Notes
- All data is **mock/dummy** and fictional; names are invented for demonstration.
- The intent matcher favors simple language; unexpected phrasing returns a helpful hint with examples.

## AI features (optional)

This project can optionally use OpenAI to power the `/chat` endpoint and to generate flashcards.

1. Create a `.env` file in the project root (or copy `.env.example`) and set:

```
OPENAI_API_KEY=sk-...your-key-here...
```

2. Install dependencies and run the app as before. If `OPENAI_API_KEY` is not set, the `/chat` endpoint will fall back to the rule-based logic and `/flashcards` will build simple cards from the local DB.

Security: Never commit your real `.env` or API keys into version control. Use the `.env.example` to show required variables.

## How to test the AI endpoints

1. Start the server (see Quickstart above)
2. Visit http://127.0.0.1:8000/ and use the UI tabs to switch between Rule-based Ask, AI Chat and Flashcards.
3. To test without UI, use curl or HTTPie to POST to `/chat` or GET `/flashcards`.

Example (PowerShell):

```powershell
curl -X GET http://127.0.0.1:8000/flashcards
```

If `OPENAI_API_KEY` is not set the `/chat` endpoint will return a rule-based answer and `/flashcards` will use the DB fallback.

## Deployment notes

- When deploying to a remote host, set `OPENAI_API_KEY` in the host environment (not in `.env`).
- Use a process manager (gunicorn/uvicorn workers) or a container for production.
- Consider adding logging, rate-limiting, and API key management if you expose the chat to public users.
