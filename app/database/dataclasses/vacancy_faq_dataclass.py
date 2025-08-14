from dataclasses import dataclass
from app.database.configuration.connection import get_connection

VACANCY_FAQ_KEY = 'vacancy_faq'


@dataclass
class VacancyFAQ:
    id: int
    vacancy_id: int
    question: str
    answer: str

    @staticmethod
    def format_question(question: str) -> str:
        """Обрезает вопрос, если он слишком длинный."""
        return f"{question[:20]}..." if len(question) > 22 else question

    @classmethod
    def get_by_vacancy_id(cls, vacancy_id: int) -> list["VacancyFAQ"]:
        """Получает все FAQ по конкретной вакансии."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, vacancy_id, question, answer FROM faq WHERE vacancy_id = ?",
            (vacancy_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row[0], vacancy_id=row[1], question=row[2], answer=row[3]) for row in rows]

    @classmethod
    def get_by_id(cls, faq_id: int) -> "VacancyFAQ | None":
        """Получает FAQ по ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, vacancy_id, question, answer FROM faq WHERE id = ?",
            (faq_id,)
        )
        row = cursor.fetchone()
        conn.close()
        return cls(id=row[0], vacancy_id=row[1], question=row[2], answer=row[3]) if row else None
