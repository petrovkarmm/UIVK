from app.database.configuration.connection import get_connection


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # name, phone, org_itn, org_name deleting
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT,
        telegram_first_name TEXT,
        telegram_last_name TEXT,
        telegram_username TEXT,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS firm (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        firm_type TEXT NOT NULL CHECK (firm_type IN ('legal_entity', 'individual')),
        last_selected BOOLEAN,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS firm_info_legal_entity (
        firm_id INTEGER PRIMARY KEY,
        organization_name TEXT,
        organization_representative_name TEXT,
        organization_itn TEXT,
        phone TEXT,
        FOREIGN KEY (firm_id) REFERENCES firm(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS firm_info_individual (
        firm_id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        FOREIGN KEY (firm_id) REFERENCES firm(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pyrus_token (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pyrus_login TEXT,
        pyrus_security_key TEXT UNIQUE,
        access_token TEXT,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS technical_problem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        hidden BOOLEAN DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_user_id INTEGER,
        user_firstname TEXT,
        user_lastname TEXT,
        user_username TEXT,
        feedback_text TEXT,
        viewed BOOLEAN DEFAULT 0,
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()