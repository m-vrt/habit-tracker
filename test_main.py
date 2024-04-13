import unittest
from unittest.mock import patch
from io import StringIO
from main import main


class TestMain(unittest.TestCase):
    @patch('builtins.input', side_effect=['1', 'New Habit', 'Description', 'daily', '9'])  
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_habit(self, mock_stdout, mock_input):
        main()
        expected_output = "New habit to add: Habit description: Daily or Weekly?: Exiting the Habit Tracker...\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
