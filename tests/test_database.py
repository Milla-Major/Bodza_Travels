import sqlite3, os, tempfile, pytest, database
from database import save_search, get_recent_places


ORIGINAL_DB_PATH = database.DB_PATH

@pytest.fixture
def temp_db():
    #tempdb
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        test_path = tf.name

    with sqlite3.connect(test_path) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

    database.DB_PATH = test_path
    yield  
    os.remove(test_path)
    database.DB_PATH = ORIGINAL_DB_PATH

def test_save_and_get_recent_places(temp_db):
    save_search("Szombathely")
    save_search("Budapest")
    save_search("Szombathely")

    results = get_recent_places()
    assert ("Szombathely", 2) in results
    assert ("Budapest", 1) in results
    assert len(results) == 2
