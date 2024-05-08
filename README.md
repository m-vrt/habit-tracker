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


## GitHub Repository

The GitHub repository for this project can be found at [`m-vrt/habit-tracker`](https://github.com/m-vrt/habit-tracker).