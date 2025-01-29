import sqlite3

from ..utils.db_utils import get_db_connection
from .study_calendar_model import get_study_calendar
from .tasks_model import get_tasks


def insert_task_progress(task_day, task_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO task_progress (task_day, task_id, status)
        VALUES (?, ?, ?)
    """,
        (task_day, task_id, status),
    )
    conn.commit()
    conn.close()


def get_task_progress():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT task_day_id, task_day, task_id, status 
        FROM task_progress 
        ORDER BY task_day, task_id
    """)
    progress = cursor.fetchall()
    conn.close()
    return [dict(p) for p in progress]


def update_task_progress(task_day_id, task_day, task_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE task_progress
        SET task_day = ?, task_id = ?, status = ?
        WHERE task_day_id = ?
    """,
        (task_day, task_id, status, task_day_id),
    )
    conn.commit()
    conn.close()


def populate_task_progress():
    try:
        # Retrieve all tasks and study_calendar entries
        tasks = get_tasks()
        study_calendar = get_study_calendar()

        if not tasks:
            print(
                "No tasks found. Please ensure that tasks are inserted before "
                "populating task_progress."
            )
            return

        if not study_calendar:
            print(
                "No study calendar entries found. Please ensure that study_calendar "
                "is populated before populating task_progress."
            )
            return

        # Connect to the database once for all insertions
        conn = get_db_connection()
        cursor = conn.cursor()

        # Iterate through all study days and tasks to insert task_progress entries
        for day in study_calendar:
            day_number = day["day_number"]
            for task in tasks:
                task_id = task["task_id"]
                status = "open"

                try:
                    cursor.execute(
                        """
                        INSERT INTO task_progress (task_day, task_id, status)
                        VALUES (?, ?, ?)
                    """,
                        (day_number, task_id, status),
                    )
                except sqlite3.IntegrityError as ie:
                    print(
                        f"IntegrityError: {ie} - Skipping duplicate entry for "
                        f"task_day {day_number} and task_id {task_id}."
                    )

        # Commit all insertions and close the connection
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"SQLite Error during population: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred during population: {ex}")


def get_diary():
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # SQL JOIN between task_progress and tasks tables
        cursor.execute("""
            SELECT 
                tp.task_day, 
                tp.status, 
                t.name, 
                t.type
            FROM 
                task_progress tp
            INNER JOIN 
                tasks t
            ON 
                tp.task_id = t.task_id
            ORDER BY 
                tp.task_day, t.type, t.name
        """)

        diary_entries = cursor.fetchall()
        conn.close()

        # Convert fetched data to a list of dictionaries
        diary = [
            {
                "task_day": entry["task_day"],
                "status": entry["status"],
                "name": entry["name"],
                "type": entry["type"],
            }
            for entry in diary_entries
        ]
        return diary

    except sqlite3.Error as e:
        print(f"SQLite Error in get_diary: {e}")
        return []
    except Exception as ex:
        print(f"An unexpected error occurred in get_diary: {ex}")
        return []
