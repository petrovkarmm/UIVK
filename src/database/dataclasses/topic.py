from dataclasses import dataclass
from datetime import datetime
from src.database.configuration.connection import get_connection


@dataclass
class Topic:
    id: int
    user_id: int
    topic_id: int
    created: str
    updated: str

    @classmethod
    def create(cls, user_id: int, topic_id: int) -> "Topic":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO topic (user_id, topic_id) 
            VALUES (?, ?)
        """, (user_id, topic_id))
        conn.commit()

        topic_id_db = cursor.lastrowid
        cursor.execute("SELECT id, user_id, topic_id, created, updated FROM topic WHERE id = ?", (topic_id_db,))
        row = cursor.fetchone()
        conn.close()

        return cls(id=row[0], user_id=row[1], topic_id=row[2], created=row[3], updated=row[4])

    @classmethod
    def get_by_user_id(cls, user_id: int) -> "Topic | None":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, topic_id, created, updated FROM topic WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def get_by_topic_id(cls, topic_id: int) -> "Topic | None":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, topic_id, created, updated FROM topic WHERE topic_id = ?", (topic_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def update_topic_id(cls, user_id: int, new_topic_id: int) -> "Topic | None":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE topic SET topic_id = ?, updated = CURRENT_TIMESTAMP WHERE user_id = ?",
            (new_topic_id, user_id)
        )
        conn.commit()
        cursor.execute("SELECT id, user_id, topic_id, created, updated FROM topic WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

