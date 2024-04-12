import unittest
from initialize_database import main
from database import HabitDatabase

class TestInitializeDatabase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):        
        cls.db = HabitDatabase("test.db")        
        cls.db.clear_database()        
        main()

    @classmethod
    def tearDownClass(cls):       
        cls.db.close()

    def test_initialization(self):      
        habits = self.db.get_habits()       
        self.assertIn("Morning Exercise", habits)
        self.assertIn("Reading Time", habits)     
    

if __name__ == "__main__":
    unittest.main()
