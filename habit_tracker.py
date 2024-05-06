import pandas as pd
from typing import List, Dict, Any
import sqlite3

def get_habit_data_from_database() -> List[Dict[str, Any]]:
    conn = sqlite3.connect('main.db')  
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM habits")
    habit_data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    keys = ["id", "name", "description", "periodicity", "created_date", "completion_date", "completion_time"]
    habit_data_dicts = [dict(zip(keys, row)) for row in habit_data]
    
    return habit_data_dicts

def check_habit_status_daily_for_habit_tracker(habit_name, habit_data):
    habit_data = get_habit_data_from_database()
    
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
    
    return habit_status_current_month[['Date', 'Completion']]

def get_daily_habits_for_habit_tracker() -> List[Dict[str, Any]]:
    habit_data = get_habit_data_from_database()

    unique_habits = set()
    unique_daily_habits = []

    for habit in habit_data:
        if habit['periodicity'] == 'Daily':
            habit_name = habit['name']
            if habit_name not in unique_habits:
                unique_habits.add(habit_name)
                unique_daily_habits.append(habit)

    return unique_daily_habits

def check_habit_status_weekly_for_habit_tracker(habit_name, habit_data):
    habit_data = get_habit_data_from_database()
    
    habit_df = pd.DataFrame(habit_data)
    habit_df = habit_df[(habit_df['name'] == habit_name) & (habit_df['periodicity'] == 'Weekly')]
    habit_df['completion_date'] = pd.to_datetime(habit_df['completion_date'])
    
    habit_status = []
   
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
            habit_status.append({'Period': f'Week {week}:', 'Completion': f'Completed on {week_completion.date()}'})
        else:
            habit_status.append({'Period': f'Week {week}:', 'Completion': ''})

        if week == 4 and current_month_end <= week_end:
            break
        elif week == 5 and last_day_of_current_month <= week_end.day: 

            break

    return pd.DataFrame(habit_status)

def get_weekly_habits_for_habit_tracker() -> List[Dict[str, Any]]:

    habit_data = get_habit_data_from_database()

    unique_habits = set()
    unique_weekly_habits = []

    for habit in habit_data:
        if habit['periodicity'] == 'Weekly':
            habit_name = habit['name']
            if habit_name not in unique_habits:
                unique_habits.add(habit_name)
                unique_weekly_habits.append(habit)

    return unique_weekly_habits
