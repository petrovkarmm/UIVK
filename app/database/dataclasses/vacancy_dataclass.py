from dataclasses import dataclass
from app.database.configuration.connection import get_connection

VACANCY_KEY = 'vacancy'


@dataclass
class Vacancy:
    id: int
    vacancy_name: str
    hidden_status: bool

    @classmethod
    def get_all(cls) -> list["Vacancy"]:
        """Получает все вакансии из базы."""
        # TODO добавить возможность фильтра на hidden
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM vacancy")
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row[0], vacancy_name=row[1]) for row in rows]

    @classmethod
    def get_by_id(cls, vacancy_id: int) -> "Vacancy | None":
        """Получает вакансию по ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM vacancy WHERE id = ?", (vacancy_id,))
        row = cursor.fetchone()
        conn.close()
        # TODO добавить логику с hidden
        return cls(id=row[0], vacancy_name=row[1]) if row else None

    @staticmethod
    def formatted_hidden_vacancy(name: str, hidden_status: bool) -> str:
        if hidden_status:
            return f"* {name}"
        else:
            return name

    @staticmethod
    def format_name(name: str) -> str:
        """Обрезает название вакансии, если оно слишком длинное."""
        return f"{name[:20]}..." if len(name) > 22 else name
