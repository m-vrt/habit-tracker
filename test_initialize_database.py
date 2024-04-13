import unittest
from io import StringIO
import sys
from initialize_database import initialize_database
from database import HabitDatabase
from unittest.mock import patch

class TestInitializeDatabase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):        
        cls.db = HabitDatabase(":memory:")
        initialize_database(cls.db)

    @classmethod
    def tearDownClass(cls):       
        cls.db.close()

    def test_initialization(self):      
        habits = self.db.get_habits()       
        self.assertIn("Daily Exercise", habits)
        self.assertIn("Reading Time", habits)     

if __name__ == "__main__":
    unittest.main()
