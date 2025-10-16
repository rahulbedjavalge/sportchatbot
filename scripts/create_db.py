from pathlib import Path
import sqlite3

root = Path(__file__).resolve().parents[1]
db_path = root / "data" / "sportchat.db"
seed_path = root / "data" / "seed.sql"

print(f"Creating DB at {db_path} ...")
conn = sqlite3.connect(db_path)
with open(seed_path, "r", encoding="utf-8") as f:
    sql = f.read()
conn.executescript(sql)
conn.commit()
conn.close()
print("Done.")
