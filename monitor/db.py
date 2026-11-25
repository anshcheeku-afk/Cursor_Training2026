"""SQLite helpers for server inventory."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any

from flask import Flask, current_app, g


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_e: BaseException | None = None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app: Flask) -> None:
    app.teardown_appcontext(close_db)
    with app.app_context():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS servers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hostname TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL
            )
            """
        )
        db.commit()


def list_servers() -> list[dict[str, Any]]:
    rows = get_db().execute(
        "SELECT id, hostname, created_at FROM servers ORDER BY id ASC"
    ).fetchall()
    return [dict(r) for r in rows]


def count_servers() -> int:
    row = get_db().execute("SELECT COUNT(*) AS c FROM servers").fetchone()
    return int(row["c"])


def add_server(hostname: str) -> int:
    created = datetime.now(timezone.utc).isoformat()
    cur = get_db().execute(
        "INSERT INTO servers (hostname, created_at) VALUES (?, ?)",
        (hostname, created),
    )
    get_db().commit()
    return int(cur.lastrowid)


def delete_server(server_id: int) -> bool:
    cur = get_db().execute("DELETE FROM servers WHERE id = ?", (server_id,))
    get_db().commit()
    return cur.rowcount > 0
