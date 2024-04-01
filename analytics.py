import sqlite3

def calculate_count(db: sqlite3.Connection, counter: str) -> int:
    """
    Calculates the count of the counter.

    :param db: an initialized SQLite database connection
    :param counter: name of the counter present in the DB
    :return: length of the counter increment events
    """
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM tracker WHERE counterName = ?", (counter,))
    count = cursor.fetchone()[0]
    return count
