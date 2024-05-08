import pandas as pd
from habit_tracker import get_habit_data_from_database
from habit_tracker_predefined import check_habit_status_predefined_daily, check_habit_status_predefined_weekly




def calculate_longest_streak_for_habit_daily(habit_name, habit_data):   
    habit_df = pd.DataFrame(habit_data)
    habit_df = habit_df[(habit_df['name'] == habit_name) & (habit_df['periodicity'] == 'Daily')]
    habit_df['completion_date'] = pd.to_datetime(habit_df['completion_date'])
     
    created_date = pd.to_datetime(habit_df['created_date'].iloc[0]).date()
    current_date = pd.Timestamp.now().date()
    end_of_first_month = pd.Timestamp(created_date.year, created_date.month, 1) + pd.offsets.MonthEnd(0)
    end_of_first_month = pd.Timestamp(end_of_first_month)
    current_date = pd.Timestamp(current_date)
    
    if created_date.year == current_date.year and created_date.month == current_date.month:
        date_range_current_month = pd.date_range(start=created_date, end=end_of_first_month, freq='D')
    else:
        date_range_current_month = pd.date_range(start=current_date.replace(day=1), end=current_date, freq='D')
       
    habit_status_current_month = pd.DataFrame({'Date': date_range_current_month})
    habit_status_current_month = pd.merge(habit_status_current_month, habit_df, left_on='Date', right_on='completion_date', how='left')    
    habit_status_current_month['Completion'] = habit_status_current_month['completion_time'].apply(lambda x: 'Completed' if pd.notnull(x) else '')    
       
    current_streak = 0
    longest_streak = 0
    for completion in habit_status_current_month['Completion']:
        if completion == 'Completed':
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 0
    
    return longest_streak     

def calculate_longest_streak_for_habit_weekly(habit_name, habit_data):  
    habit_df = pd.DataFrame(habit_data)
    habit_df = habit_df[(habit_df['name'] == habit_name) & (habit_df['periodicity'] == 'Weekly')]
    habit_df['completion_date'] = pd.to_datetime(habit_df['completion_date'])
       
    current_streak = 0
    longest_streak = 0
       
    created_date = pd.to_datetime(habit_df['created_date'].iloc[0]).date()  
        
    current_month_end = pd.Timestamp.now().replace(day=1) + pd.offsets.MonthEnd(0)
    last_day_of_current_month = (pd.Timestamp.now().replace(day=1) + pd.offsets.MonthEnd(0)).day
       
    for week in range(1, 6):     
        week_start = created_date + pd.DateOffset(days=(week - 1) * 7)
        week_end = min(created_date + pd.DateOffset(days=week * 7), current_month_end)  
        week_completion = habit_df[
            (habit_df['completion_date'] >= week_start) & (habit_df['completion_date'] < week_end)
        ]['completion_date'].max()

        if pd.notnull(week_completion):
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 0
               
        if week == 4 and current_month_end <= week_end:
            break
        elif week == 5 and last_day_of_current_month <= week_end.day: 
            break
    
    return longest_streak

def calculate_longest_streak_for_habit_predefined_daily(habit_name):
    habit_status = check_habit_status_predefined_daily(habit_name)
    longest_streak = 0
    current_streak = 0
    
    for completion in habit_status['Completion']:
        if completion == 'Completed':
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 0

    longest_streak = max(longest_streak, current_streak)
    
    return longest_streak

def calculate_longest_streak_for_habit_predefined_weekly(habit_name):
    habit_status = check_habit_status_predefined_weekly(habit_name)
    longest_streak = 0
    current_streak = 0
    
    for completion in habit_status['Completion']:
        if completion != '':
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 0

    longest_streak = max(longest_streak, current_streak)
    
    return longest_streak

def get_habit_hall_of_fame_daily():
    """Get the longest streak among all daily habits."""
    habit_data = get_habit_data_from_database()
    daily_habits = [habit['name'] for habit in habit_data if habit['periodicity'] == 'Daily']
    
    longest_streak = 0
    for habit_name in daily_habits:
        streak = calculate_longest_streak_for_habit_daily(habit_name, habit_data)
        longest_streak = max(longest_streak, streak)
    
    return longest_streak

def get_habit_hall_of_fame_weekly():
    """Get the longest streak among all weekly habits."""
    habit_data = get_habit_data_from_database()
    weekly_habits = [habit['name'] for habit in habit_data if habit['periodicity'] == 'Weekly']
    
    longest_streak = 0
    for habit_name in weekly_habits:
        streak = calculate_longest_streak_for_habit_weekly(habit_name, habit_data)
        longest_streak = max(longest_streak, streak)
    
    return longest_streak

def get_habits_with_longest_streaks(periodicity):
    """Get habits with the longest streaks for the given periodicity."""
    habit_data = get_habit_data_from_database()
    unique_habits = set() 

    if periodicity == "Daily":
        for habit in habit_data:
            if habit['periodicity'] == 'Daily':
                habit_name = habit['name']
                streak = calculate_longest_streak_for_habit_daily(habit_name, habit_data)
                unique_habits.add((habit_name, streak))
    elif periodicity == "Weekly":
        for habit in habit_data:
            if habit['periodicity'] == 'Weekly':
                habit_name = habit['name']
                streak = calculate_longest_streak_for_habit_weekly(habit_name, habit_data)
                unique_habits.add((habit_name, streak))

    if not unique_habits:
        return []

    longest_streak = max([habit[1] for habit in unique_habits])
    return [(habit[0], habit[1]) for habit in unique_habits if habit[1] == longest_streak]



