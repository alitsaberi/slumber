from utils.db_utils import get_db_connection

def insert_study_calendar(study_date, day_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO study_calendar (study_date, day_number)
        VALUES (?, ?)
    ''', (study_date, day_number))
    conn.commit()
    conn.close()

def get_study_calendar():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT study_date, day_number FROM study_calendar')
    calendar = cursor.fetchall()
    conn.close()
    return calendar

def update_study_calendar(study_date, day_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE study_calendar
        SET day_number = ?
        WHERE study_date = ?
    ''', (day_number, study_date))
    conn.commit()
    conn.close()