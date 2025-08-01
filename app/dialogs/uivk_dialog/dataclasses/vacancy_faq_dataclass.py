from dataclasses import dataclass

VACANCY_FAQ_KEY = 'vacancy_faq'


@dataclass
class VacancyFAQ:
    id: int
    question: str
