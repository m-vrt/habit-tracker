import pytest
from habit_tracker import HabitTracker

def test_remove_habit_when_list_empty():
    tracker = HabitTracker()
    assert len(tracker.get_habits()) == 0
   
    tracker.remove_habit("Exercise")
    assert len(tracker.get_habits()) == 0

def test_check_habit_state_when_no_habits_tracked():
    tracker = HabitTracker()
    assert tracker.check_habit_state("Exercise") == "No habits tracked"

def test_view_streaks_when_no_habits_completed():
    tracker = HabitTracker()
    assert tracker.view_streaks() == {}
