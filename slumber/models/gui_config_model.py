import sqlite3

from ..utils.database import get_db_connection


def get_gui_config():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT font_size, app_width, app_height, app_mode, language 
        FROM gui_config 
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def update_gui_config(font_size, app_width, app_height, app_mode, language):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE gui_config
        SET font_size = ?, app_width = ?, app_height = ?, app_mode = ?, language = ?
        WHERE rowid = 1
    """,
        (font_size, app_width, app_height, app_mode, language),
    )
    conn.commit()
    conn.close()


def insert_default_gui_config(font_size, app_width, app_height, app_mode, language):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO gui_config (font_size, app_width, app_height, app_mode, language)
        VALUES (?, ?, ?, ?, ?)
    """,
        (font_size, app_width, app_height, app_mode, language),
    )
    conn.commit()
    conn.close()
