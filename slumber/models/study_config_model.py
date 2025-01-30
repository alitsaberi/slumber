import sqlite3

from ..utils.database import get_db_connection


def insert_study_config(study_duration, start_date, end_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO study_config (study_duration, start_date, end_date)
        VALUES (?, ?, ?)
    """,
        (study_duration, start_date, end_date),
    )
    conn.commit()
    conn.close()


def get_study_config():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT study_duration, start_date, end_date FROM study_config LIMIT 1"
    )
    config = cursor.fetchone()
    conn.close()
    if config:
        return dict(config)
    return None


def update_study_config(study_duration, start_date, end_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE study_config
        SET study_duration = ?, start_date = ?, end_date = ?
        WHERE rowid = 1
    """,
        (study_duration, start_date, end_date),
    )
    conn.commit()
    conn.close()
