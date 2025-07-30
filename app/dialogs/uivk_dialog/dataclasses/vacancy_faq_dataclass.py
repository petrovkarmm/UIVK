from dataclasses import dataclass

VacancyFAQ_key = 'vacancy_faq'


@dataclass
class VacancyFAQ:
    id: int
    question: str
