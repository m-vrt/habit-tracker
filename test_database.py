import pytest
from datetime import datetime
from database import HabitDatabase

@pytest.fixture(scope="module")
def habit_db():
    """Create a HabitDatabase instance for testing."""
    db = HabitDatabase(":memory:")  
    yield db
    db.close()

def test_create_tables(habit_db):
    """Test database initialization and table creation."""
    cursor = habit_db.connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='habits'")
    assert cursor.fetchone() is not None
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='predefined_data'")
    assert cursor.fetchone() is not None

def test_add_habit(habit_db):
    """Test adding a habit to the database."""
    habit_db.add_habit("Exercise", "Daily exercise routine", "Daily")
    cursor = habit_db.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM habits WHERE name='Exercise'")
    assert cursor.fetchone()[0] == 1

def test_delete_habit(habit_db):
    """Test deleting a habit from the database."""
    habit_db.delete_habit("Exercise", datetime.now().strftime("%m/%d/%Y %H:%M"))
    cursor = habit_db.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM habits WHERE name='Exercise'")
    assert cursor.fetchone()[0] == 0


