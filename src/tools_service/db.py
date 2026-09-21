from pathlib import Path

import aiosqlite

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    order_id    TEXT PRIMARY KEY,
    customer    TEXT NOT NULL,
    status      TEXT NOT NULL,
    eta         TEXT,
    last_update TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS processed_events (
    event_id    TEXT PRIMARY KEY,
    received_at TEXT NOT NULL
);
"""

SEED_ORDERS = [
    ("ORD-1001", "Ana Gomez", "in_transit", "2026-09-24", "2026-09-21T09:15:00Z"),
    ("ORD-1002", "Luis Perez", "delivered", None, "2026-09-20T17:40:00Z"),
    ("ORD-1003", "Maria Ruiz", "processing", "2026-09-26", "2026-09-21T08:02:00Z"),
    ("ORD-1004", "Jorge Diaz", "cancelled", None, "2026-09-19T12:30:00Z"),
]


async def init_db(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(path) as db:
        await db.executescript(SCHEMA)
        await db.executemany("INSERT OR IGNORE INTO orders VALUES (?, ?, ?, ?, ?)", SEED_ORDERS)
        await db.commit()


async def fetch_order(path: str, order_id: str) -> dict | None:
    """Day 4: return the order as a dict, or None if it does not exist.

    Hints:
      - open a connection with `aiosqlite.connect(path)`
      - set `db.row_factory = aiosqlite.Row` so rows behave like dicts
      - use a parameterised query (never an f-string) to avoid SQL injection
    """
    raise NotImplementedError("Day 4")
