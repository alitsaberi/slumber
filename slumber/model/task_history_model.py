from utils.db_utils import get_db_connection

def insert_task_history(timestamp, description, activity, task_day_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO task_history (timestamp, description, activity, task_day_id)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, description, activity, task_day_id))
    conn.commit()
    conn.close()

def get_task_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT history_id, timestamp, description, activity, task_day_id FROM task_history')
    history = cursor.fetchall()
    conn.close()
    return history

def update_task_history(history_id, timestamp, description, activity, task_day_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE task_history
        SET timestamp = ?, description = ?, activity = ?, task_day_id = ?
        WHERE history_id = ?
    ''', (timestamp, description, activity, task_day_id, history_id))
    conn.commit()
    conn.close()