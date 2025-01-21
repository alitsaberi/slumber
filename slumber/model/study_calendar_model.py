import sqlite3
from datetime import datetime, timedelta

from ..utils.db_utils import get_db_connection


def get_study_calendar():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT study_date, day_number FROM study_calendar')
    calendar = cursor.fetchall()
    conn.close()
    return [dict(c) for c in calendar]


def populate_study_calendar(study_duration, start_date):
    try:        
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert new entries
        for day in range(study_duration):
            current_date = start_date + timedelta(days=day)
            study_date = current_date.strftime('%Y-%m-%d') 
            day_number = day + 1
            cursor.execute('''
                INSERT INTO study_calendar (study_date, day_number)
                VALUES (?, ?)
            ''', (study_date, day_number))
        
        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        
        print(f"Study calendar populated with {study_duration} days from {start_date}.")
    
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

def get_todays_day_number():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    today_str = datetime.now().strftime('%Y-%m-%d')
    cursor.execute(
        "SELECT day_number FROM study_calendar WHERE study_date = ?", (today_str,)
    )
    row = cursor.fetchone()
    
    conn.close()
    return row["day_number"] if row else None