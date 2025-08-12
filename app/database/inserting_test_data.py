from app.database.configuration.connection import get_connection


def insert_test_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Добавляем вакансии
    vacancies = [
        ("Python Developer",),
        ("Frontend Developer",),
        ("Data Analyst",)
    ]
    cursor.executemany("INSERT INTO vacancy (title) VALUES (?)", vacancies)

    # Получаем ID вставленных вакансий
    cursor.execute("SELECT id, title FROM vacancy")
    vacancy_rows = cursor.fetchall()

    # Добавляем FAQ для каждой вакансии
    faq_data = []
    for vac_id, title in vacancy_rows:
        faq_data.append((vac_id, f"Что делает {title}?", f"{title} занимается своими делами."))
        faq_data.append((vac_id, f"Какие навыки нужны {title}?", "Опыт, желание и немного кофе."))

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
