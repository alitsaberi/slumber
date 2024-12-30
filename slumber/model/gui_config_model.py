from utils.db_utils import get_db_connection

def get_gui_config():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT font_size, app_width, app_height, app_mode FROM gui_config LIMIT 1')
    config = cursor.fetchone()
    conn.close()
    return config

def update_gui_config(font_size, app_width, app_height, app_mode):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE gui_config
        SET font_size = ?, app_width = ?, app_height = ?, app_mode = ?
        WHERE rowid = 1
    ''', (font_size, app_width, app_height, app_mode))
    conn.commit()
    conn.close()