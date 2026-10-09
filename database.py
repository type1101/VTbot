import sqlite3

def initdb():
    connexion = sqlite3.connect("veille.db")
    cursor = connexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT UNIQUE,
            title TEXT
        )
    """)
    connexion.commit()
    connexion.close()