from utils.db_utils import get_db_connection

def insert_task_progress(task_day, task_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO task_progress (task_day, task_id, status)
        VALUES (?, ?, ?)
    ''', (task_day, task_id, status))
    conn.commit()
    conn.close()

def get_task_progress():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT task_day_id, task_day, task_id, status FROM task_progress')
    progress = cursor.fetchall()
    conn.close()
    return progress

def update_task_progress(task_day_id, task_day, task_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE task_progress
        SET task_day = ?, task_id = ?, status = ?
        WHERE task_day_id = ?
    ''', (task_day, task_id, status, task_day_id))
    conn.commit()
    conn.close()