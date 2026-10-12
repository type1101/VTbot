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

def is_article_new(link):
    connexion = sqlite3.connect("veille.db")
    cursor = connexion.cursor()
    cursor.execute("SELECT * FROM articles WHERE link = ?", (link,))
    result = cursor.fetchone()
    connexion.close()
    return result is None

def save_article(link, title):
    connexion = sqlite3.connect("veille.db")
    cursor = connexion.cursor()
    cursor.execute("INSERT INTO articles (link, title) VALUES (?, ?)", (link, title))
    connexion.commit()
    connexion.close()