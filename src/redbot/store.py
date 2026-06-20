from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator


@dataclass(frozen=True)
class KnowledgeHit:
    id: int
    title: str
    content: str
    source: str


@dataclass(frozen=True)
class ChatMessage:
    channel: str
    conversation_id: str
    user_id: str
    text: str
    direction: str
    created_at: str


class RedbotStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _raw_connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = self._raw_connect()
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    scope TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (scope, key)
                );

                CREATE TABLE IF NOT EXISTS knowledge_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    source TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel TEXT NOT NULL,
                    conversation_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    text TEXT NOT NULL,
                    direction TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

    def save_memory(self, scope: str, key: str, value: str) -> None:
        now = _now()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO memories(scope, key, value, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(scope, key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = excluded.updated_at
                """,
                (scope, key.strip(), value.strip(), now),
            )

    def get_memory(self, scope: str, key: str) -> str | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT value FROM memories WHERE scope = ? AND key = ?",
                (scope, key),
            ).fetchone()
        return str(row["value"]) if row else None

    def list_memories(self, scope: str) -> dict[str, str]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT key, value FROM memories WHERE scope = ? ORDER BY key",
                (scope,),
            ).fetchall()
        return {str(row["key"]): str(row["value"]) for row in rows}

    def add_document(self, title: str, content: str, source: str = "manual") -> int:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO knowledge_documents(title, content, source, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (title.strip(), content.strip(), source.strip(), _now()),
            )
            return int(cursor.lastrowid)

    def search_knowledge(self, query: str, limit: int = 5) -> list[KnowledgeHit]:
        terms = [term.lower() for term in query.split() if term.strip()]
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, title, content, source
                FROM knowledge_documents
                ORDER BY id DESC
                """
            ).fetchall()
        scored: list[tuple[int, sqlite3.Row]] = []
        for row in rows:
            haystack = f"{row['title']} {row['content']}".lower()
            score = sum(1 for term in terms if term in haystack)
            if score:
                scored.append((score, row))
        scored.sort(key=lambda item: (-item[0], -int(item[1]["id"])))
        return [
            KnowledgeHit(
                id=int(row["id"]),
                title=str(row["title"]),
                content=str(row["content"]),
                source=str(row["source"]),
            )
            for _, row in scored[:limit]
        ]

    def record_message(
        self,
        channel: str,
        conversation_id: str,
        user_id: str,
        text: str,
        direction: str,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO messages(channel, conversation_id, user_id, text, direction, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (channel, conversation_id, user_id, text, direction, _now()),
            )

    def recent_messages(self, channel: str, conversation_id: str, limit: int = 10) -> list[ChatMessage]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT channel, conversation_id, user_id, text, direction, created_at
                FROM messages
                WHERE channel = ? AND conversation_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (channel, conversation_id, limit),
            ).fetchall()
        return [
            ChatMessage(
                channel=str(row["channel"]),
                conversation_id=str(row["conversation_id"]),
                user_id=str(row["user_id"]),
                text=str(row["text"]),
                direction=str(row["direction"]),
                created_at=str(row["created_at"]),
            )
            for row in reversed(rows)
        ]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
