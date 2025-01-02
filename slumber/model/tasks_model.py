import sqlite3

from utils.db_utils import get_db_connection


def insert_task(name, header, module, type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (name, header, module, type)
        VALUES (?, ?, ?, ?)
    ''', (name, header, module, type))
    conn.commit()
    conn.close()

def get_tasks():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT task_id, name, header, module, type 
        FROM tasks 
        ORDER BY task_id
    ''')
    tasks = cursor.fetchall()
    conn.close()
    return [{key: task[key] for key in task} for task in tasks]

def update_task(task_id, name, header, module, type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks
        SET name = ?, header = ?, module = ?, type = ?
        WHERE task_id = ?
    ''', (name, header, module, type, task_id))
    conn.commit()
    conn.close()