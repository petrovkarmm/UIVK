from dataclasses import dataclass
from app.database.configuration.connection import get_connection

VACANCY_KEY = 'vacancy'


@dataclass
class Vacancy:
    id: int
    vacancy_name: str
    hidden_status: bool

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
    def get_all(cls, include_hidden: bool = True) -> list["Vacancy"]:
        """Получает все вакансии. Если include_hidden=False, то только не скрытые."""
        conn = get_connection()
        cursor = conn.cursor()
        if include_hidden:
            cursor.execute("SELECT id, title, hidden FROM vacancy")
        else:
            cursor.execute("SELECT id, title, hidden FROM vacancy WHERE hidden = 0")
        rows = cursor.fetchall()
        conn.close()
        return [
            cls(id=row[0], vacancy_name=row[1], hidden_status=bool(row[2]))
            for row in rows
        ]

    @classmethod
    def get_by_id(cls, vacancy_id: int) -> "Vacancy | None":
        """Получает вакансию по ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, hidden FROM vacancy WHERE id = ?", (vacancy_id,)
        )
        row = cursor.fetchone()
        conn.close()
        return (
            cls(id=row[0], vacancy_name=row[1], hidden_status=bool(row[2]))
            if row else None
        )
