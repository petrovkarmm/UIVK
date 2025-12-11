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
    media: Optional[dict] = None

    @staticmethod
    def format_question(question: str) -> str:
        return f"{question[:20]}..." if len(question) > 22 else question

    @classmethod
    def _from_row(cls, row) -> "VacancyFAQ":
        return cls(
            id=row[0],
            vacancy_id=row[1],
            question=row[2],
            answer=row[3],
            created=row[4],
            updated=row[5],
            media=json.loads(row[6]) if row[6] else None
        )

    @classmethod
    def get_by_vacancy_id(cls, vacancy_id: int) -> list["VacancyFAQ"]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, vacancy_id, question, answer, created, updated, media FROM faq WHERE vacancy_id = ?",
            (vacancy_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def get_by_id(cls, faq_id: int) -> Optional["VacancyFAQ"]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, vacancy_id, question, answer, created, updated, media FROM faq WHERE id = ?",
            (faq_id,)
        )
        row = cursor.fetchone()
        conn.close()
        return cls._from_row(row) if row else None

    @classmethod
    def create_new(cls, vacancy_id: int, question: str, answer: str, media: Optional[dict] = None) -> "VacancyFAQ":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO faq (vacancy_id, question, answer, media) VALUES (?, ?, ?, ?)",
            (vacancy_id, question, answer, json.dumps(media) if media else None)
        )
        conn.commit()

        new_id = cursor.lastrowid
        cursor.execute(
            "SELECT id, vacancy_id, question, answer, created, updated, media FROM faq WHERE id = ?",
            (new_id,)
        )
        row = cursor.fetchone()
        conn.close()
        return cls._from_row(row)

    @classmethod
    def delete_by_id(cls, faq_id: int) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM faq WHERE id = ?", (faq_id,))
        conn.commit()
        conn.close()

    @classmethod
    def update_question(cls, faq_id: int, new_question: str) -> Optional["VacancyFAQ"]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE faq SET question = ?, updated = CURRENT_TIMESTAMP WHERE id = ?",
            (new_question, faq_id)
        )
        conn.commit()

        cursor.execute(
            "SELECT id, vacancy_id, question, answer, created, updated, media FROM faq WHERE id = ?",
            (faq_id,)
        )
        row = cursor.fetchone()
        conn.close()

        return cls._from_row(row) if row else None

    @classmethod
    def update_answer(cls, faq_id: int, new_answer: str) -> Optional["VacancyFAQ"]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE faq SET answer = ?, updated = CURRENT_TIMESTAMP WHERE id = ?",
            (new_answer, faq_id)
        )
        conn.commit()

        cursor.execute(
            "SELECT id, vacancy_id, question, answer, created, updated, media FROM faq WHERE id = ?",
            (faq_id,)
        )
        row = cursor.fetchone()
        conn.close()

        return cls._from_row(row) if row else None
