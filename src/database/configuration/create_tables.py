from src.database.configuration.connection import get_connection


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Вакансии
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacancy (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        hidden BOOLEAN DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Админы
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Таблица топиков (user_id ↔ topic_id)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS topic (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        topic_id INTEGER NOT NULL UNIQUE,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Таблица группы (одна запись!)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_group (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL
    )
    """)

    # Вопросы и ответы, связанные с вакансией
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faq (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vacancy_id INTEGER NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        media JSON DEFAULT NULL,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (vacancy_id) REFERENCES vacancy(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
