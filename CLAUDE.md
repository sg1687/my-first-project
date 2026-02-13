# CLAUDE.md

## Project Overview

A learning project with Python scripts and Flask REST APIs for task management.

## Project Structure

- `hello.py`, `hello_world.py` — Introductory Python scripts
- `calculator.py` — CLI calculator
- `my-first-api/app.py` — Flask REST API (task CRUD)
- `todo-api/app.py` — Todo List API with full CRUD (port 5000)
- `todo-api/index.html` — Frontend for the Todo API
- `workout-tracker/app.py` — Workout Tracker API with full CRUD (port 5001)
- `workout-tracker/index.html` — Frontend for the Workout Tracker
- `index.html` — HTML frontend

## Tech Stack

- Python 3
- Flask (API framework)
- flask-cors (cross-origin support)

## How to Run

```bash
# Run Python scripts
python3 hello.py
python3 calculator.py

# Run the Task API
cd my-first-api
source venv/bin/activate
python app.py  # Starts on port 8000

# Run the Todo API
pip3 install flask flask-cors
cd todo-api
python3 app.py  # Starts on port 5000

# Run the Workout Tracker
pip3 install flask flask-cors
cd workout-tracker
python3 app.py  # Starts on port 5001
```

## Conventions

- Use f-strings for string formatting
- Keep scripts simple and readable
- Add comments explaining what each line does
