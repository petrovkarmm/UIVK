from dataclasses import dataclass
from src.database.configuration.connection import get_connection


@dataclass
class ChatGroup:
    id: int
    group_id: int
    general_topic_id: int

    @classmethod
    def create(cls, group_id: int, general_topic_id: int) -> "ChatGroup":
        conn = get_connection()
        cursor = conn.cursor()
        # гарантируем, что запись только одна
        cursor.execute("DELETE FROM chat_group")
        cursor.execute("""
            INSERT INTO chat_group (group_id, general_topic_id) 
            VALUES (?, ?)
        """, (group_id, general_topic_id))
        conn.commit()

        cursor.execute("SELECT id, group_id, general_topic_id FROM chat_group LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return cls(*row)

    @classmethod
    def get(cls) -> "ChatGroup | None":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, group_id, general_topic_id FROM chat_group LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def update(cls, group_id: int = None, general_topic_id: int = None) -> "ChatGroup":
        conn = get_connection()
        cursor = conn.cursor()
        if group_id:
            cursor.execute("UPDATE chat_group SET group_id = ? WHERE id = 1", (group_id,))
        if general_topic_id:
            cursor.execute("UPDATE chat_group SET general_topic_id = ? WHERE id = 1", (general_topic_id,))
        conn.commit()

        cursor.execute("SELECT id, group_id, general_topic_id FROM chat_group LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return cls(*row)
