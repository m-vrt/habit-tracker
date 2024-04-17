from database import HabitDatabase

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

    def store(self, habit_database: HabitDatabase) -> None:
        """Store the counter in the database."""
        habit_database.add_counter(self.name, self.description)

    def add_event(self, habit_database: HabitDatabase, date: str = None) -> None:
        """Add an event to the counter in the database."""
        habit_database.increment_counter(self.name, date)        
        streak = habit_database.get_streak_for_habit(self.name)
        if streak is not None:
            habit_database.update_streak(self.name, streak + 1)
        else:
            habit_database.update_streak(self.name, 1)
