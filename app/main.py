from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
import os
from typing import List, Optional
from pydantic import BaseModel
import aiosqlite

# Create the FastAPI app
app = FastAPI(title="Todo App")

# Setup templates and static files
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Database setup
DATABASE_FILE = "todo.db"

async def init_db():
    # Create database if it doesn't exist
    if not os.path.exists(DATABASE_FILE):
        async with aiosqlite.connect(DATABASE_FILE) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    completed BOOLEAN NOT NULL DEFAULT 0
                )
            ''')
            await db.commit()

async def get_db():
    db = await aiosqlite.connect(DATABASE_FILE)
    try:
        yield db
    finally:
        await db.close()

# Models
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool

# Routes
@app.get("/")
async def read_root(request: Request, db: aiosqlite.Connection = Depends(get_db)):
    async with db.execute("SELECT id, title, description, completed FROM todos") as cursor:
        todos = await cursor.fetchall()
    
    # Convert to list of dictionaries
    todo_list = [
        {"id": row[0], "title": row[1], "description": row[2], "completed": bool(row[3])}
        for row in todos
    ]
    
    return templates.TemplateResponse(
        "index.html", {"request": request, "todos": todo_list}
    )

@app.post("/todos/")
async def create_todo(
    title: str = Form(...),
    description: str = Form(""),
    db: aiosqlite.Connection = Depends(get_db)
):
    await db.execute(
        "INSERT INTO todos (title, description) VALUES (?, ?)",
        (title, description)
    )
    await db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/todos/{todo_id}/toggle")
async def toggle_todo(
    todo_id: int,
    db: aiosqlite.Connection = Depends(get_db)
):
    # Get current status
    async with db.execute("SELECT completed FROM todos WHERE id = ?", (todo_id,)) as cursor:
        result = await cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Todo not found")
        current_status = result[0]
    
    # Toggle status
    new_status = not bool(current_status)
    await db.execute(
        "UPDATE todos SET completed = ? WHERE id = ?",
        (int(new_status), todo_id)
    )
    await db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/todos/{todo_id}/delete")
async def delete_todo(
    todo_id: int,
    db: aiosqlite.Connection = Depends(get_db)
):
    await db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    await db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.on_event("startup")
async def startup():
    await init_db()

# Run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 