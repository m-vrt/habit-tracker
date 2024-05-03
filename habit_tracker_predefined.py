import pandas as pd
from typing import List, Dict, Any


habit_data = [
    {"id": 1, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/1/2024", "completion_time": "23:29:27"},
    {"id": 2, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/2/2024", "completion_time": "20:42:14"},
    {"id": 3, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/3/2024", "completion_time": "23:22:10"},
    {"id": 4, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/4/2024", "completion_time": "21:19:07"},
    {"id": 5, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/5/2024", "completion_time": "21:36:08"},
    {"id": 6, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/6/2024", "completion_time": "23:04:19"},
    {"id": 7, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/7/2024", "completion_time": "18:11:22"},
    {"id": 8, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/8/2024", "completion_time": "18:19:06"},
    {"id": 9, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/9/2024", "completion_time": "21:36:18"},
    {"id": 10, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/10/2024", "completion_time": "23:09:34"},
    {"id": 11, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/11/2024", "completion_time": "22:58:46"},
    {"id": 12, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/12/2024", "completion_time": "18:13:04"},
    {"id": 13, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/13/2024", "completion_time": "22:57:48"},
    {"id": 14, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/14/2024", "completion_time": "22:22:21"},
    {"id": 15, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/15/2024", "completion_time": "21:17:18"},
    {"id": 16, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/16/2024", "completion_time": "22:48:41"},
    {"id": 17, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/17/2024", "completion_time": "19:30:14"},
    {"id": 18, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/18/2024", "completion_time": "23:37:11"},
    {"id": 19, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/19/2024", "completion_time": "17:42:44"},
    {"id": 20, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/20/2024", "completion_time": "23:01:01"},
    {"id": 21, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/21/2024", "completion_time": "20:26:58"},
    {"id": 22, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/22/2024", "completion_time": "18:48:23"},
    {"id": 23, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/23/2024", "completion_time": "17:40:35"},
    {"id": 24, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/24/2024", "completion_time": "17:52:19"},
    {"id": 25, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/25/2024", "completion_time": "21:24:15"},
    {"id": 26, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/26/2024", "completion_time": "22:18:29"},
    {"id": 27, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/27/2024", "completion_time": "18:42:58"},
    {"id": 28, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/28/2024", "completion_time": "20:49:58"},
    {"id": 29, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/29/2024", "completion_time": "23:03:59"},
    {"id": 30, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/30/2024", "completion_time": "20:36:40"},
    {"id": 31, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/31/2024", "completion_time": "19:38:33"},
    {"id": 32, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/6/2024", "completion_time": "18:23:58"},
    {"id": 33, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/8/2024", "completion_time": "23:45:55"},
    {"id": 34, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/10/2024", "completion_time": "23:54:24"},
    {"id": 35, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/11/2024", "completion_time": "19:10:49"},
    {"id": 36, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/14/2024", "completion_time": "20:38:30"},
    {"id": 37, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/15/2024", "completion_time": "20:39:34"},
    {"id": 38, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/16/2024", "completion_time": "20:09:50"},
    {"id": 39, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/17/2024", "completion_time": "20:02:30"},
    {"id": 40, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/18/2024", "completion_time": "19:18:46"},
    {"id": 41, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/20/2024", "completion_time": "19:10:33"},
    {"id": 42, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/21/2024", "completion_time": "21:21:25"},
    {"id": 43, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/22/2024", "completion_time": "18:15:29"},
    {"id": 44, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/24/2024", "completion_time": "19:16:59"},
    {"id": 45, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/25/2024", "completion_time": "22:10:45"},
    {"id": 46, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/26/2024", "completion_time": "21:16:17"},
    {"id": 47, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/27/2024", "completion_time": "19:26:26"},
    {"id": 48, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/28/2024", "completion_time": "23:28:29"},
    {"id": 49, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/29/2024", "completion_time": "18:16:09"},
    {"id": 50, "name": "Research", "description": "Do some research", "periodicity": "Daily", "created_date": "3/3/2024 17:37", "completion_date": "3/4/2024", "completion_time": "20:37:55"},
    {"id": 51, "name": "Research", "description": "Do some research", "periodicity": "Daily", "created_date": "3/3/2024 17:37", "completion_date": "3/8/2024", "completion_time": "21:34:43"},
    {"id": 52, "name": "Research", "description": "Do some research", "periodicity": "Daily", "created_date": "3/3/2024 17:37", "completion_date": "3/9/2024", "completion_time": "20:04:03"},
    {"id": 53, "name": "Research", "description": "Do some research", "periodicity": "Daily", "created_date": "3/3/2024 17:37", "completion_date": "3/10/2024", "completion_time": "20:54:25"},
    {"id": 54, "name": "Research", "description": "Do some research", "periodicity": "Daily", "created_date": "3/3/2024 17:37", "completion_date": "3/12/2024", "completion_time": "21:17:42"},
    {"id": 55, "name": "Research", "description": "Do some research", "periodicity": "Daily", "created_date": "3/3/2024 17:37", "completion_date": "3/13/2024", "completion_time": "18:27:14"},
    {"id": 56, "name": "Research", "description": "Do some research", "periodicity": "Daily", "created_date": "3/3/2024 17:37", "completion_date": "3/14/2024", "completion_time": "19:52:30"},
    {"id": 57, "name": "Research", "description": "Do some research", "periodicity": "Daily", "created_date": "3/3/2024 17:37", "completion_date": "3/18/2024", "completion_time": "19:25:57"},
    {"id": 58, "name": "Research", "description": "Do some research", "periodicity": "Daily", "created_date": "3/3/2024 17:37", "completion_date": "3/19/2024", "completion_time": "22:09:03"},
    {"id": 59, "name": "Research", "description": "Do some research", "periodicity": "Daily", "created_date": "3/3/2024 17:37", "completion_date": "3/20/2024", "completion_time": "20:48:28"},
    {"id": 60, "name": "Research", "description": "Do some research", "periodicity": "Daily", "created_date": "3/3/2024 17:37", "completion_date": "3/21/2024", "completion_time": "21:26:37"},
    {"id": 61, "name": "Research", "description": "Do some research", "periodicity": "Daily", "created_date": "3/3/2024 17:37", "completion_date": "3/22/2024", "completion_time": "23:28:29"},
    {"id": 62, "name": "Research", "description": "Do some research", "periodicity": "Daily", "created_date": "3/3/2024 17:37", "completion_date": "3/29/2024", "completion_time": "22:06:05"},
    {"id": 63, "name": "Research", "description": "Do some research", "periodicity": "Daily", "created_date": "3/3/2024 17:37", "completion_date": "3/30/2024", "completion_time": "19:24:46"},
    {"id": 64, "name": "Clean House", "description": "Do household chores", "periodicity": "Weekly", "created_date": "3/1/2024 19:45", "completion_date": "3/1/2024", "completion_time": "21:55:33"},
    {"id": 65, "name": "Clean House", "description": "Do household chores", "periodicity": "Weekly", "created_date": "3/1/2024 19:45", "completion_date": "3/6/2024", "completion_time": "21:40:37"},
    {"id": 66, "name": "Clean House", "description": "Do household chores", "periodicity": "Weekly", "created_date": "3/1/2024 19:45", "completion_date": "3/19/2024", "completion_time": "21:26:50"},
    {"id": 67, "name": "Call Family", "description": "Check in with family members", "periodicity": "Weekly", "created_date": "3/4/2024 16:15", "completion_date": "3/9/2024", "completion_time": "23:59:59"},
    {"id": 68, "name": "Call Family", "description": "Check in with family members", "periodicity": "Weekly", "created_date": "3/4/2024 16:15", "completion_date": "3/16/2024", "completion_time": "19:30:45"},
    {"id": 69, "name": "Call Family", "description": "Check in with family members", "periodicity": "Weekly", "created_date": "3/4/2024 16:15", "completion_date": "3/23/2024", "completion_time": "20:15:29"},
    {"id": 70, "name": "Call Family", "description": "Check in with family members", "periodicity": "Weekly", "created_date": "3/4/2024 16:15", "completion_date": "3/30/2024", "completion_time": "18:50:18"},
]



def check_habit_status_predefined_daily(habit_name):   
    habit_df = pd.DataFrame(habit_data)
    habit_df = habit_df[(habit_df['name'] == habit_name) & (habit_df['periodicity'] == 'Daily')]    
    habit_df['completion_date'] = pd.to_datetime(habit_df['completion_date'], format='%m/%d/%Y')    
    habit_status = habit_df.groupby('completion_date').apply(lambda x: 'Completed' if x['completion_time'].notnull().any() else '').reset_index()   
    habit_status.columns = ['Date', 'Completion']
    date_range = pd.date_range(start='3/1/2024', end='3/31/2024')   
    habit_status = pd.merge(pd.DataFrame(date_range, columns=['Date']), habit_status, on='Date', how='left')    
    habit_status['Completion'] = habit_status['Completion'].fillna('')
    return habit_status

def get_predefined_daily_habits(habit_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Get the list of unique predefined daily habits."""
    unique_habits = set()
    unique_predefined_daily_habits = []

    for habit in habit_data:
        if habit['periodicity'] == 'Daily':
            habit_name = habit['name']
            if habit_name not in unique_habits:
                unique_habits.add(habit_name)
                unique_predefined_daily_habits.append(habit)

    return unique_predefined_daily_habits