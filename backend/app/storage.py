# backend/app/storage.py
import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).parent.parent / "data" / "itineraries.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS itineraries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        json TEXT
    )""")
    conn.commit()
    conn.close()

def save_itinerary(title: str, json_text: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO itineraries (title,json) VALUES (?,?)", (title, json_text))
    conn.commit()
    conn.close()
