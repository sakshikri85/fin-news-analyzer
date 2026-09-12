"""
database.py
Lightweight SQLite storage so the analyzer can keep a history of sector
signals over time (useful for charts in the dashboard and for auditing
why a signal changed). Uses only the Python standard library.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

from signal_engine import SectorSignal

DB_PATH = Path(__file__).parent / "signals_history.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS sector_signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recorded_at TEXT NOT NULL,
    sector TEXT NOT NULL,
    avg_sentiment REAL NOT NULL,
    signal TEXT NOT NULL,
    confidence_pct REAL NOT NULL,
    article_count INTEGER NOT NULL
);
"""


class SignalDatabase:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(SCHEMA)
            conn.commit()

    def save_signals(self, signals: Dict[str, SectorSignal]) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        rows = [
            (
                timestamp,
                sig.sector,
                sig.avg_sentiment,
                sig.signal,
                sig.confidence_pct,
                sig.article_count,
            )
            for sig in signals.values()
        ]
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO sector_signals
                   (recorded_at, sector, avg_sentiment, signal, confidence_pct, article_count)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                rows,
            )
            conn.commit()

    def load_history(self, sector: str | None = None, limit: int = 200):
        query = "SELECT recorded_at, sector, avg_sentiment, signal, confidence_pct, article_count FROM sector_signals"
        params: tuple = ()
        if sector:
            query += " WHERE sector = ?"
            params = (sector,)
        query += " ORDER BY recorded_at DESC LIMIT ?"
        params = params + (limit,)
        with self._connect() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()


if __name__ == "__main__":
    db = SignalDatabase()
    print(f"Database ready at: {db.db_path}")
