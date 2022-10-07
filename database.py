from typing import Any, Tuple, List
import sqlite3
import os

PATH = 'db'
DATABASE = f'{PATH}/base.db'


def create():
    with sqlite3.connect('db/base.db') as connect:
        cur = connect.cursor()
        sql = 'CREATE TABLE IF NOT EXISTS radio('\
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
            'name TEXT NOT NULL, '\
            'url TEXT NOT NULL'\
            ');'
        cur.execute(sql)

        sql = 'CREATE TABLE IF NOT EXISTS dashboard('\
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
            'radio_id INTEGER NOT NULL, '\
            'url TEXT NOT NULL'\
            'FOREIGN KEY (radio_id) REFERENCES radio(id) '\
            'ON DELETE CASCADE'\
            ');'
        cur.execute(sql)

        sql = 'CREATE TABLE IF NOT EXISTS dashboard_data('\
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
            'dashboard_id INTEGER NOT NULL, '\
            'token TEXT NOT NULL'\
            'FOREIGN KEY (radio_id) REFERENCES radio(id) '\
            'ON DELETE CASCADE'\
            ');

        connect.commit()
        cur.close()


if not os.path.isdir(PATH):
    os.makedirs(PATH)
    create()
    

def insert_radio(name: str, url: str) -> int:
    with sqlite3.connect(DATABASE) as connect:
        cur = connect.cursor()

        sql = 'INSERT INTO radio(name, url) VALUES(?, ?);'
        cur.execute(sql, (name, url))
        result = cur.lastrowid
        connect.commit()
        cur.close()
    return result


def insert_dashboard(radio_id: int, url: str) -> int:
    with sqlite3.connect(DATABASE) as connect:
        cur = connect.cursor()

        sql = 'INSERT INTO dashboard(radio_id, url) VALUES(?, ?);'
        cur.execute(sql, (radio_id, url))
        result = cur.lastrowid
        connect.commit()
        cur.close()
    return result


def insert_dashboard_options():
    pass


def select_radio(name: str,) -> Tuple[Any] | None:
    with sqlite3.connect(DATABASE) as connect:
        cur = connect.cursor()
        sql = 'SELECT * FROM radio WHERE name = ?;'
        cur.execute(sql, (name,))
        result = cur.fetchone()
        cur.close()
    return result


def select_dashboard(radio_id: int) -> Tuple[Any] | None:
    with sqlite3.connect(DATABASE) as connect:
        cur = connect.cursor()
        sql = 'SELECT * FROM dashboard WHERE radio_id = ?;'
        cur.execute(sql, (radio_id,))
        result = cur.fetchone()
        cur.close()
    return result


def select_all_radio_names() -> Tuple[tuple[str]] | None:
    with sqlite3.connect(DATABASE) as connect:
        cur = connect.cursor()
        sql = 'SELECT name FROM radio;'
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
    return result
