# Habit Tracker

This is a basic habit tracker portfolio project built in Python, developed as a university requirement for the course Object Oriented and Functional Programming with Python.


## Installation

1. Clone the repository:

```
git clone https://github.com/m-vrt/habit-tracker.git
```

2. Navigate to the project directory:

```
cd habit-tracker
```

3. Set up a virtual environment:

```
python3 -m venv venv
```
 
4. Activate the virtual environment:
- On Windows:

```
venv\Scripts\activate
```

- On macOS and Linux:

```
source venv/bin/activate
```

5. Install project dependencies:

```
pip install -r requirements.txt
```


## Development Environment

This project was developed using Visual Studio Code (VS Code).


## Requirements

- Python >= 3.12.2
- SQLite3


## Usage

Run the following command to start the application:

```
python main.py
```

Follow the on-screen prompts to manage your habits.


## Testing

### Using Pytest

To run tests for different test modules separately, you can use pytest along with the test module name.

For example, to run tests for the `test_habit_tracker.py` module:

```
pytest test_habit_tracker.py
```

If you want to run all tests across all test modules:

```
pytest
```


## Populating Predefined Data

The `predefined_data` table contains predefined habits populated from the `predefined_data.csv` file. To achieve this, the following steps were taken:

1. **Initial Population:** The data from the `predefined_data.csv` file was imported into the `predefined_data` table using SQLite3.

2. **Instructions for Populating the Table:**

   If you want to populate the `predefined_data` table with data from the `predefined_data.csv` file, you can follow these steps using SQLite3 or a tool like DB Browser:

   - **Using SQLite3 Command Line:**

     Make sure you have the `predefined_data.csv` file available in the project directory. Then, execute the following command in your terminal:

     ```bash
     sqlite3 main.db ".mode csv" ".import predefined_data.csv predefined_data"
     ```

     This command will import the data from the CSV file into the `predefined_data` table in the SQLite database (`main.db`).

   - **Using DB Browser:**

     1. Open DB Browser and load the `main.db` file.
     2. Navigate to the "Import" option in the menu.
     3. Select the `predefined_data.csv` file.
     4. Choose the `predefined_data` table as the destination.
     5. Proceed with the import process.

   After completing these steps, the `predefined_data` table will be populated with the data from the CSV file.


## GitHub Repository

The GitHub repository for this project can be found at [`m-vrt/habit-tracker`](https://github.com/m-vrt/habit-tracker).