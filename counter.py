import sqlite3

class Counter:
    def __init__(self, name: str, description: str):
        """Counter class, to count events

        :param name: the name of the counter
        :param description: the description
        """
        self.name = name
        self.description = description
        self.count = 0

    def increment(self) -> None:
        """Increment the counter by 1."""
        self.count += 1

    def reset(self) -> None:
        """Reset the counter to 0."""
        self.count = 0

    def store(self, db: sqlite3.Connection) -> None:
        """Store the counter in the database."""
        cursor = db.cursor()
        cursor.execute("INSERT INTO counter VALUES (?, ?)", (self.name, self.description))
        db.commit()

    def add_event(self, db: sqlite3.Connection, date: str = None) -> None:
        """Add an event to the counter in the database."""
        cursor = db.cursor()
        cursor.execute("INSERT INTO tracker VALUES (?, ?)", (date, self.name))
        db.commit()
