from dataclasses import dataclass
from app.database.configuration.connection import get_connection

VACANCY_KEY = 'vacancy'


@dataclass
class Vacancy:
    id: int
    vacancy_name: str

    @staticmethod
    def format_name(name: str) -> str:
        """Обрезает название вакансии, если оно слишком длинное."""
        return f"{name[:20]}..." if len(name) > 22 else name

    @classmethod
    def get_all(cls) -> list["Vacancy"]:
        """Получает все вакансии из базы."""
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
        return cls(id=row[0], vacancy_name=row[1]) if row else None
