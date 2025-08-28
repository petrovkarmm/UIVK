from dataclasses import dataclass
from typing import Optional, List
from app.database.configuration.connection import get_connection


@dataclass
class Admin:
    id: int
    telegram_id: int

    @classmethod
    def add(cls, telegram_id: int) -> bool:
        """Добавить нового админа. Возвращает True, если добавлен, False если уже есть."""
        conn = get_connection()
        cursor = conn.cursor()

        # Проверим, существует ли уже такой админ
        cursor.execute("SELECT id FROM admin WHERE telegram_id = ?", (telegram_id,))
        if cursor.fetchone():
            conn.close()
            return False  # уже существует

        cursor.execute("INSERT INTO admin (telegram_id) VALUES (?)", (telegram_id,))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def delete(cls, telegram_id: int) -> bool:
        """Удалить админа по telegram_id. Возвращает True, если удалён, False если не найден."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM admin WHERE telegram_id = ?", (telegram_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False  # не найден

        cursor.execute("DELETE FROM admin WHERE telegram_id = ?", (telegram_id,))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def exists(cls, telegram_id: int) -> bool:
        """Проверка, есть ли админ в базе."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM admin WHERE telegram_id = ?", (telegram_id,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    @classmethod
    def all(cls) -> List["Admin"]:
        """Вернуть список всех админов"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, telegram_id FROM admin")
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row[0], telegram_id=row[1]) for row in rows]
