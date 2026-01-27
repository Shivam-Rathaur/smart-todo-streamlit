# database.py
import sqlite3
from datetime import datetime

DB_NAME = "tasks.db"

## connection
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

## create Table (safe)
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'Pending',
            due_date TEXT,
            priority INTEGER DEFAULT 3,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    conn.commit()
    conn.close()

### add task 
def add_task(title, description, due_date=None, priority=3):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO tasks (title, description, status, due_date, priority, created_at, updated_at)
        VALUES (?, ?, 'Pending', ?, ?, ?, ?)
    """, (title, description, due_date, priority, now, now))

    conn.commit()
    conn.close()

### get all tasks
def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, description, status, due_date, priority, created_at, updated_at
        FROM tasks
    """)

    tasks = cursor.fetchall()
    conn.close()
    return tasks

### update status
def update_status(task_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET status = ?, updated_at = ?
        WHERE id = ?
    """, (status, datetime.now().isoformat(), task_id))

    conn.commit()
    conn.close()

## update task
def update_task(task_id, title, description, due_date, priority):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET title = ?, description = ?, due_date = ?, priority = ?, updated_at = ?
        WHERE id = ?
    """, (
        title,
        description,
        due_date,
        priority,
        datetime.now().isoformat(),
        task_id
    ))

    conn.commit()
    conn.close()

### delete task
def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
