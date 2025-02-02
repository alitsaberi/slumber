import sqlite3
from pathlib import Path

from slumber import settings


def get_db_connection():
    db_path = Path("../../") / settings["database"]["name"]
    return sqlite3.connect(db_path)


def initialize_db():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Create tables with enums defined directly
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gui_config (
            font_size INTEGER CHECK(font_size >= 0 AND font_size <= 10),
            app_width INTEGER,
            app_height INTEGER,
            app_mode TEXT CHECK(app_mode IN ('window', 'full_screen')),
            language VARCHAR
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_config (
            study_duration INTEGER,
            start_date DATE,
            end_date DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_calendar (
            study_date DATE,
            day_number INTEGER
        )
    """)
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS tasks (
    #         task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         name VARCHAR,
    #         header VARCHAR,
    #         module VARCHAR,
    #         type TEXT CHECK(
    #             type IN ('pre_processing', 'post_processing', 'action', 'recording')
    #         )
    #     )
    # """)
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS task_progress (
    #         task_day_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         task_day INTEGER,
    #         task_id INTEGER,
    #         status TEXT CHECK(status IN ('progress', 'open', 'closed')),
    #         FOREIGN KEY (task_day) REFERENCES study_calendar(day_number),
    #         FOREIGN KEY (task_id) REFERENCES tasks(task_id)
    #     )
    # """)
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS task_history (
    #         history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         timestamp TIMESTAMP,
    #         description VARCHAR,
    #         activity VARCHAR,
    #         task_day_id INTEGER,
    #         FOREIGN KEY (task_day_id) REFERENCES task_progress(task_day_id)
    #     )
    # """)

    connection.commit()
    connection.close()
