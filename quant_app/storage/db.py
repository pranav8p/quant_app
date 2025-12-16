import sqlite3
from threading import Lock

class TickDB:
    def __init__(self, db_path="ticks.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.lock = Lock()
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS ticks (
                timestamp INTEGER,
                symbol TEXT,
                price REAL,
                qty REAL
            )
        """)
        self.conn.commit()

    def insert_ticks(self, ticks):
        with self.lock:
            self.conn.executemany(
                "INSERT INTO ticks VALUES (?, ?, ?, ?)",
                [
                    (t["timestamp"], t["symbol"], t["price"], t["qty"])
                    for t in ticks
                ]
            )
            self.conn.commit()
