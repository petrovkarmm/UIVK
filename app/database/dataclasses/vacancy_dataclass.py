from dataclasses import dataclass
from typing import Optional, List

from app.database.configuration.connection import get_connection

VACANCY_KEY = 'vacancy'


@dataclass
class Vacancy:
    id: int
    vacancy_name: str
    hidden_status: bool
    created: str
    updated: str

    @staticmethod
    def format_name(name: str) -> str:
        """Обрезает название вакансии, если оно слишком длинное."""
        return f"{name[:20]}..." if len(name) > 23 else name

    @staticmethod
    def formatted_hidden_vacancy(name: str, hidden_status: bool) -> str:
        """Форматирует название вакансии с учётом скрытого статуса."""
        formatted_name = Vacancy.format_name(name)
        return f"🔒 {formatted_name}" if hidden_status else formatted_name

    @classmethod
    def get_all(cls, include_hidden: bool = True) -> List["Vacancy"]:
        """Получает все вакансии. Если include_hidden=False, то только не скрытые."""
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT id, title, hidden, created, updated FROM vacancy"
        if not include_hidden:
            query += " WHERE hidden = 0"

        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        return [
            cls(id=row[0], vacancy_name=row[1], hidden_status=bool(row[2]),
                created=row[3], updated=row[4])
            for row in rows
        ]

    @classmethod
    def get_by_id(cls, vacancy_id: int) -> Optional["Vacancy"]:
        """Получает вакансию по ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, hidden, created, updated FROM vacancy WHERE id = ?", (vacancy_id,)
        )
        row = cursor.fetchone()
        conn.close()

        return (
            cls(id=row[0], vacancy_name=row[1], hidden_status=bool(row[2]),
                created=row[3], updated=row[4])
            if row else None
        )

    @classmethod
    def delete_by_id(cls, vacancy_id: int) -> bool:
        """Удаляет вакансию по ID. Возвращает True, если удаление прошло успешно."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vacancy WHERE id = ?", (vacancy_id,))
        conn.commit()
        rows_deleted = cursor.rowcount
        conn.close()

        return rows_deleted > 0
