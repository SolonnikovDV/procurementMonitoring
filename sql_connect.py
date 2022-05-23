import sqlite3
import config as cfg


def sql_connect():
    conn = sqlite3.connect(cfg.db_file_name)
    cur = conn.cursor()
    return cur
