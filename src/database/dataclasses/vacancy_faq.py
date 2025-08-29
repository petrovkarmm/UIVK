import json
from dataclasses import dataclass
from typing import Optional

from src.database.configuration.connection import get_connection

VACANCY_FAQ_KEY = 'vacancy_faq'


@dataclass
class VacancyFAQ:
    id: int
    vacancy_id: int
    question: str
    answer: str
    created: str
    updated: str
    file_id: Optional[str] = None  # только один файл

    @staticmethod
    def format_question(question: str) -> str:
        """Обрезает вопрос, если он слишком длинный."""
        return f"{question[:20]}..." if len(question) > 22 else question

    @classmethod
    def get_by_vacancy_id(cls, vacancy_id: int) -> list["VacancyFAQ"]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, vacancy_id, question, answer, created, updated, file_id FROM faq WHERE vacancy_id = ?",
            (vacancy_id,)
        )
        rows = cursor.fetchall()
        conn.close()

        return [
            cls(
                id=row[0],
                vacancy_id=row[1],
                question=row[2],
                answer=row[3],
                created=row[4],
                updated=row[5],
                file_id=row[6] if row[6] else None
            )
            for row in rows
        ]

    @classmethod
    def get_by_id(cls, faq_id: int) -> Optional["VacancyFAQ"]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, vacancy_id, question, answer, created, updated, file_id FROM faq WHERE id = ?",
            (faq_id,)
        )
        row = cursor.fetchone()
        conn.close()

        return cls(
            id=row[0],
            vacancy_id=row[1],
            question=row[2],
            answer=row[3],
            created=row[4],
            updated=row[5],
            file_id=row[6] if row[6] else None
        ) if row else None

    @classmethod
    def create_new(cls, vacancy_id: int, question: str, answer: str, file_id: Optional[str] = None) -> "VacancyFAQ":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO faq (vacancy_id, question, answer, file_id) VALUES (?, ?, ?, ?)",
            (vacancy_id, question, answer, file_id)
        )
        conn.commit()

        new_id = cursor.lastrowid
        cursor.execute(
            "SELECT id, vacancy_id, question, answer, created, updated, file_id FROM faq WHERE id = ?",
            (new_id,)
        )
        row = cursor.fetchone()
        conn.close()

        return cls(
            id=row[0],
            vacancy_id=row[1],
            question=row[2],
            answer=row[3],
            created=row[4],
            updated=row[5],
            file_id=row[6] if row[6] else None
        )

    @classmethod
    def delete_by_id(cls, faq_id: int) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM faq WHERE id = ?", (faq_id,))
        conn.commit()
        conn.close()
