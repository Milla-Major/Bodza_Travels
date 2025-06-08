import sqlite3

DB_PATH = "data/btravels.db"


def save_search(city_name):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO searches (city_name) VALUES (?)", (city_name,))
        conn.commit()

def get_recent_places(limit=20):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT city, COUNT(*) as count
            FROM searches
            GROUP BY city
            ORDER BY count DESC
            LIMIT ?
        """, (limit,))
        return c.fetchall()
