from dataclasses import dataclass

VACANCY_KEY = 'vacancy'


@dataclass
class Vacancy:
    id: int
    vacancy_name: str

