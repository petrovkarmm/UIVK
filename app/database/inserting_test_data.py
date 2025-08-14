from app.database.configuration.connection import get_connection


def insert_test_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Добавляем вакансии с флагом hidden по умолчанию 0
    vacancies = [
        ("Python Developer", 0),
        ("Frontend Developer", 0),
        ("Data Analyst", 1),  # Сделаем одну скрытую для примера
    ]
    cursor.executemany("INSERT INTO vacancy (title, hidden) VALUES (?, ?)", vacancies)

    # Получаем ID и название вставленных вакансий
    cursor.execute("SELECT id, title FROM vacancy")
    vacancy_rows = cursor.fetchall()

    # Набор вопросов/ответов для каждой вакансии
    faq_templates = {
        "Python Developer": [
            ("Чем занимается Python Dev?", "Пишет backend, автоматизацию и скрипты."),
            ("Какие фреймворки нужны?", "Django, FastAPI, Flask."),
            ("Нужен ли опыт в DevOps?", "Желателен, особенно Docker и CI/CD."),
        ],
        "Frontend Developer": [
            ("Что делает Frontend Dev?", "Разрабатывает интерфейсы и UI."),
            ("Какие технологии важны?", "React, TypeScript, HTML, CSS."),
        ],
        "Data Analyst": [
            ("Чем занимается аналитик?", "Собирает, обрабатывает и анализирует данные."),
            ("Какие инструменты нужны?", "SQL, Excel, Power BI, Python."),
            ("Нужен ли опыт в ML?", "Будет плюсом, но не обязателен."),
            ("Что с визуализацией?", "Tableau, Matplotlib, Seaborn."),
        ]
    }

    # Добавляем FAQ
    faq_data = []
    for vac_id, title in vacancy_rows:
        if title in faq_templates:
            for question, answer in faq_templates[title]:
                faq_data.append((vac_id, question, answer))

    cursor.executemany(
        "INSERT INTO faq (vacancy_id, question, answer) VALUES (?, ?, ?)",
        faq_data
    )

    conn.commit()
    conn.close()
    print("✅ Тестовые данные добавлены.")


if __name__ == "__main__":
    insert_test_data()
    print("🚀 Всё готово!")
