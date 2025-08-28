from dataclasses import dataclass
from typing import Optional, List

from src.database.configuration.connection import get_connection

VACANCY_KEY = 'vacancy'


@dataclass
class Vacancy:
    id: int
    title: str
    hidden: bool
    created: str
    updated: str

    @staticmethod
    def format_title(title: str) -> str:
        """Обрезает название вакансии, если оно слишком длинное."""
        return f"{title[:20]}..." if len(title) > 23 else title

    @staticmethod
    def format_hidden_button(hidden: bool) -> str:
        return f"🔒 вакансия скрыта" if hidden else '🔓 вакансия видна'

    @staticmethod
    def formatted_title_hidden_vacancy(title: str, hidden: bool) -> str:
        """Форматирует название вакансии с учётом скрытого статуса."""
        formatted_title = Vacancy.format_title(title)
        return f"🔒 {formatted_title}" if hidden else formatted_title

    @classmethod
    def toggle_hidden(cls, vacancy_id: int) -> None:
        """Переключает статус hidden у вакансии по её id."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT hidden FROM vacancy WHERE id = ?", (vacancy_id,))
        row = cursor.fetchone()

        if row is None:
            conn.close()
            raise ValueError(f"Vacancy with id={vacancy_id} not found")

        new_status = not bool(row[0])
        cursor.execute("UPDATE vacancy SET hidden = ?, updated = CURRENT_TIMESTAMP WHERE id = ?",
                       (new_status, vacancy_id))
        conn.commit()
        conn.close()

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
            cls(
                id=row[0],
                title=row[1],
                hidden=bool(row[2]),
                created=row[3],
                updated=row[4]
            )
            for row in rows
        ]

    @classmethod
    def get_by_id(cls, vacancy_id: int) -> Optional["Vacancy"]:
        """Получает вакансию по ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, hidden, created, updated FROM vacancy WHERE id = ?",
            (vacancy_id,)
        )
        row = cursor.fetchone()
        conn.close()

        return (
            cls(
                id=row[0],
                title=row[1],
                hidden=bool(row[2]),
                created=row[3],
                updated=row[4]
            )
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

    @classmethod
    def create_new(cls, title: str) -> "Vacancy":
        """Создаёт новую вакансию и возвращает объект."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO vacancy (title, hidden) VALUES (?, ?)",
            (title, 1)
        )
        conn.commit()

        new_id = cursor.lastrowid
        cursor.execute(
            "SELECT id, title, hidden, created, updated FROM vacancy WHERE id = ?",
            (new_id,)
        )
        row = cursor.fetchone()
        conn.close()

        return cls(
            id=row[0],
            title=row[1],
            hidden=bool(row[2]),
            created=row[3],
            updated=row[4]
        )
