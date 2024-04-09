import pytest
from unittest.mock import MagicMock
from habit_tracker import HabitTracker
from habit import Habit
from database import HabitDatabase

class TestHabitTracker:
    @pytest.fixture
    def habit_tracker(self):
        habit_database = MagicMock(spec=HabitDatabase)
        tracker = HabitTracker(habit_database)
        tracker.habits = []
        yield tracker
        tracker.close_database()

    def test_add_habit(self, habit_tracker: HabitTracker):
        habit_tracker.habit_database.add_habit = MagicMock()
        habit = Habit("Exercise", "Do workout for 30 minutes", "daily", "2024-04-01")
        habit_tracker.add_habit(habit)
        assert len(habit_tracker.get_habits()) == 1

    def test_remove_habit(self, habit_tracker: HabitTracker):
        habit_tracker.habit_database.remove_habit = MagicMock()
        habit_tracker.habit_database.get_habits.side_effect = [["Exercise"], []]
        habit_tracker.remove_habit("Exercise")
        assert len(habit_tracker.get_habits()) == 0

    def test_check_habit_state_with_habits_tracked(self, habit_tracker: HabitTracker):
        habit_tracker.habit_database.get_habits = MagicMock(return_value=["Exercise"])
        assert habit_tracker.check_habit_state("Exercise") == "Habit exists"

    def test_check_habit_state_when_no_habits_tracked(self, habit_tracker: HabitTracker):
        habit_tracker.habit_database.get_habits = MagicMock(return_value=[])
        assert habit_tracker.check_habit_state("Exercise") == "No habits tracked"

    def test_view_streaks_with_habits_completed(self, habit_tracker: HabitTracker):
        habit_tracker.habit_database.get_habits = MagicMock(return_value=["Exercise"])
        habit_tracker.habit_database.get_streaks = MagicMock(return_value={"Exercise": 5})
        streaks = habit_tracker.view_streaks()
        assert streaks == {'Exercise': 5}  

    def test_view_streaks_when_no_habits_completed(self, habit_tracker: HabitTracker):
        habit_tracker.habit_database.get_streaks = MagicMock(return_value={})
        streaks = habit_tracker.view_streaks()
        assert streaks == {} 
          