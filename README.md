# FastAPI Todo App

A simple Todo application built with FastAPI, SQLite, and Jinja2 templates.

## Features

- Create, complete, and delete todo items
- Modern responsive UI
- SQLite database for data storage
- FastAPI backend with async support

## Requirements

- Python 3.7+
- Dependencies listed in requirements.txt

## Setup and Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

4. Open a web browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

## Project Structure

```
app/
  ├── main.py           # FastAPI application
  ├── static/
  │   └── styles.css    # CSS styles
  └── templates/
      └── index.html    # Jinja2 template
requirements.txt        # Dependencies
todo.db                 # SQLite database (auto-created)
```

## API Endpoints

- `GET /`: Main page, displays all todos
- `POST /todos/`: Create a new todo
- `POST /todos/{todo_id}/toggle`: Toggle a todo's completion status
- `POST /todos/{todo_id}/delete`: Delete a todo

## License

This project is open source and available under the [MIT License]. 