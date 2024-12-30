from utils.db_utils import get_db_connection

def insert_task(title, module, type, schedule_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, module, type, schedule_type)
        VALUES (?, ?, ?, ?)
    ''', (title, module, type, schedule_type))
    conn.commit()
    conn.close()

def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT task_id, title, module, type, schedule_type FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks