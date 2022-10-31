import sqlite3
import psycopg2
from typing import Any, List, Tuple

from my_types.database import Engine
from my_types.database import sql_command
from my_types.database import (
    tables,
    radio,
    station_address,
    station_address_params,
    scoreboard_address,
    scoreboard_address_params,
    last_radio_scoreboard_data,
    current_radio_scoreboard_data,
    radio_activity,
    silence_group,
)


PATH = 'db'
DATABASE = f'{PATH}/DATABASE.db'


class SQLite(Engine):
    def __init__(self, db_path: str = DATABASE) -> None:
        self.__PATH = db_path

        self.tables = tables(
            radio=self.__radio,
            station_address=self.__station_address,
            station_address_params=self.__station_address_params,
            scoreboard_address=self.__scoreboard_address,
            scoreboard_address_params=self.__scoreboard_address_params,
            last_radio_scoreboard_data=self.__last_radio_scoreboard_data,
            current_radio_scoreboard_data=self.__current_radio_scoreboard_data,
            radio_activity=self.__radio_activity,
            silence_group=self.__silence_group
        )
    
    def execute(self, cmd: sql_command, data: tuple = (), method: str = "") -> int|Tuple|List|None:
        with sqlite3.connect(self.__PATH) as connect:
            cursor = connect.cursor()
            if data:
                cursor.execute(cmd, data)
            else:
                cursor.execute(cmd)

            match method:
                case "fetchone":
                    return cursor.fetchone()
                case "fetchall":
                    return cursor.fetchall()
                case "lastrowid":
                    return cursor.lastrowid
                case "commit":
                    connect.commit()

    @property
    def __radio(self) -> radio:
        create = 'CREATE TABLE IF NOT EXISTS radio('\
                    'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                    'name TEXT NOT NULL);'
        list = 'SELECT name FROM radio;'
        set = 'INSERT INTO radio(name) VALUES(?);'
        return radio(create, list, set)
    
    @property
    def __station_address(self) -> station_address:
        create = 'CREATE TABLE IF NOT EXISTS station_address('\
                    'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                    'radio_id INTEGER NOT NULL, '\
                    'url TEXT NOT NULL, '\
                    'FOREIGN KEY (radio_id) REFERENCES radio(id));'
        set = "INSERT INTO station_address(radio_id, url) VALUES(?, ?);"
        get = "SELECT url, params FROM radio "\
                "INNER JOIN station_address ON "\
                    "radio.id = station_address.radio_id AND radio.name = ? "\
                    "INNER JOIN station_address_params ON "\
                        "station_address.id = station_address_params.station_address_id;"
        return station_address(create, get, set)

    @property
    def __station_address_params(self) -> station_address_params:
        create = 'CREATE TABLE IF NOT EXISTS station_address_params('\
                    'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                    'station_address_id INTEGER NOT NULL,'\
                    'params TEXT NOT NULL, '\
                    'FOREIGN KEY (station_address_id) REFERENCES station_address(id));'
        set = "INSERT INTO station_address_params(station_address_id, params) VALUES(?, ?);"
        return station_address_params(create, set)
        
    @property
    def __scoreboard_address(self) -> scoreboard_address:
        create = 'CREATE TABLE IF NOT EXISTS scoreboard_address('\
                    'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                    'radio_id INTEGER NOT NULL,'\
                    'url TEXT NOT NULL, '\
                    'FOREIGN KEY (radio_id) REFERENCES radio(id));'
        get = "SELECT url, params FROM radio "\
                "INNER JOIN scoreboard_address ON "\
                    "radio.id = scoreboard_address.radio_id AND radio.name = ? "\
                    "INNER JOIN scoreboard_address_params ON "\
                        "scoreboard_address.id = scoreboard_address_params.scoreboard_address_id;"
        set = "INSERT INTO scoreboard_address(radio_id, url) VALUES(?, ?);"
        return scoreboard_address(create, get, set)

    @property
    def __scoreboard_address_params(self) -> scoreboard_address_params:
        create = 'CREATE TABLE IF NOT EXISTS scoreboard_address_params('\
                    'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                    'scoreboard_address_id INTEGER NOT NULL,'\
                    'params TEXT NOT NULL, '\
                    'FOREIGN KEY (scoreboard_address_id) REFERENCES scoreboard_address(id));'
        set = "INSERT INTO scoreboard_address_params(scoreboard_address_id, params) VALUES(?, ?);"
        return scoreboard_address_params(create, set)

    @property
    def __last_radio_scoreboard_data(self) -> last_radio_scoreboard_data:
        create = 'CREATE TABLE IF NOT EXISTS last_scoreboard_data('\
                    'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                    'radio_id INTEGER NOT NULL, '\
                    'data TEXT NOT NULL, '\
                    'FOREIGN KEY (radio_id) REFERENCES radio(id));'
        get = "SELECT data FROM last_scoreboard_data "\
                "INNER JOIN radio ON "\
                    "radio.id = last_scoreboard_data.radio_id AND radio.name = ?;"
        set = "INSERT INTO last_scoreboard_data (radio_id, data) "\
                "VALUES ((SELECT id from radio WHERE name = ?), ?);"
        update = "UPDATE last_scoreboard_data "\
                    "SET data = ? "\
                "WHERE last_scoreboard_data.radio_id = (SELECT id FROM radio WHERE name = ?);"
        delete = "DELETE FROM last_scoreboard_data WHERE radio_id = (SELECT id FROM radio WHERE name = ?);"
        return last_radio_scoreboard_data(create, get, set, update, delete)

    @property
    def __current_radio_scoreboard_data(self) -> current_radio_scoreboard_data:
        create = 'CREATE TABLE IF NOT EXISTS current_scoreboard_data('\
                    'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                    'radio_id INTEGER NOT NULL, '\
                    'data TEXT NOT NULL, '\
                    'FOREIGN KEY (radio_id) REFERENCES radio(id));'
        get = "SELECT data FROM current_scoreboard_data "\
                "INNER JOIN radio ON "\
                    "radio.id = current_scoreboard_data.radio_id AND radio.name = ?;"
        set = "INSERT INTO current_scoreboard_data (radio_id, data) "\
                "VALUES ((SELECT id from radio WHERE name = ?), ?);"
        update = "UPDATE current_scoreboard_data "\
                    "SET data = ? "\
                "WHERE current_scoreboard_data.radio_id = (SELECT id FROM radio WHERE name = ?);"
        delete = "DELETE FROM current_scoreboard_data WHERE radio_id = (SELECT id FROM radio WHERE name = ?);"
        return current_radio_scoreboard_data(create, get, set, update, delete)

    @property
    def __radio_activity(self) -> radio_activity:
        create = 'CREATE TABLE IF NOT EXISTS radio_activity('\
                    'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                    'radio_name TEXT NOT NULL, '\
                    'guild_id INTEGER NOT NULL, '\
                    'channel_id INTEGER NOT NULL);'
        list = "SELECT radio_name, guild_id, channel_id FROM radio_activity;"
        set = "INSERT INTO radio_activity (radio_name, guild_id, channel_id) VALUES (?, ?, ?);"
        delete = "DELETE FROM radio_activity WHERE guild_id = ?;"
        return radio_activity(create, list, set, delete)
    
    @property
    def __silence_group(self) -> silence_group:
        create = 'CREATE TABLE IF NOT EXISTS silence_group('\
                    'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                    'guild_id INTEGER NOT NULL);'
        get = "SELECT * FROM silence_group WHERE guild_id = ?;"
        set = "INSERT INTO silence_group(guild_id) VALUES(?);"
        delete = "DELETE FROM silence_group WHERE guild_id = ?;"
        return silence_group(create, get, set, delete)


class PostgreSQL(Engine):
    def __init__(self, user: str, password: str, host: str, port: int) -> None:
        self.__USER = user
        self.__PASSWORD = password
        self.__HOST = host
        self.__PORT = port

        self.__connect()

        self.tables = tables(
            radio=self.__radio,
            station_address=self.__station_address,
            station_address_params=self.__station_address_params,
            scoreboard_address=self.__scoreboard_address,
            scoreboard_address_params=self.__scoreboard_address_params,
            last_radio_scoreboard_data=self.__last_radio_scoreboard_data,
            current_radio_scoreboard_data=self.__current_radio_scoreboard_data,
            radio_activity=self.__radio_activity,
            silence_group=self.__silence_group
        )

    def __connect(self):
        self._connect = psycopg2.connect(f"user='{self.__USER}' host='{self.__HOST}' password='{self.__PASSWORD}' port='{self.__PORT}'")

    def execute(self, cmd: sql_command, data: tuple = None, method: str = None) -> Any | None:
        try:
            cursor = self._connect.cursor()
            if data:
                cursor.execute(cmd, data)
            else:
                cursor.execute(cmd)
            match method:
                case "fetchone":
                    return cursor.fetchone()
                case "fetchall":
                    return cursor.fetchall()
                case "lastrowid":
                    return cursor.fetchone()[0]
                case "commit":
                    pass
            self._connect.commit()
            cursor.close()

        except psycopg2.OperationalError:
            print("Error:", cmd, data, method)

    @property
    def __radio(self) -> radio:
        create = "CREATE TABLE IF NOT EXISTS radio("\
                    "id SERIAL PRIMARY KEY, "\
                    "name TEXT NOT NULL);"
        list = "SELECT name FROM radio;"
        set = "INSERT INTO radio (name) VALUES (%s) RETURNING id;"
        return radio(create, list, set)
    
    @property
    def __station_address(self) -> station_address:
        create = "CREATE TABLE IF NOT EXISTS station_address("\
                    "id SERIAL PRIMARY KEY, "\
                    "url TEXT NOT NULL, "\
                    "radio_id INTEGER NOT NULL, "\
                    "FOREIGN KEY(radio_id) REFERENCES radio(id));"
        set = "INSERT INTO station_address (radio_id, url) VALUES (%s, %s) RETURNING id;"
        get = "SELECT url, params FROM radio "\
                "INNER JOIN station_address ON "\
                    "radio.id = station_address.radio_id AND radio.name = %s "\
                    "INNER JOIN station_address_params ON "\
                        "station_address.id = station_address_params.station_address_id;"
        return station_address(create, get, set)

    @property
    def __station_address_params(self) -> station_address_params:
        create = "CREATE TABLE IF NOT EXISTS station_address_params("\
                    "id SERIAL PRIMARY KEY, "\
                    "params TEXT NOT NULL, "\
                    "station_address_id INTEGER REFERENCES station_address (id));"
        set = "INSERT INTO station_address_params(station_address_id, params) VALUES(%s, %s) RETURNING id;"
        return station_address_params(create, set)
        
    @property
    def __scoreboard_address(self) -> scoreboard_address:
        create = "CREATE TABLE IF NOT EXISTS scoreboard_address("\
                    "id SERIAL PRIMARY KEY, "\
                    "url TEXT NOT NULL, "\
                    "radio_id INTEGER REFERENCES radio (id));"
        get = "SELECT url, params FROM radio "\
                "INNER JOIN scoreboard_address ON "\
                    "radio.id = scoreboard_address.radio_id AND radio.name = %s "\
                    "INNER JOIN scoreboard_address_params ON "\
                        "scoreboard_address.id = scoreboard_address_params.scoreboard_address_id;"
        set = "INSERT INTO scoreboard_address(radio_id, url) VALUES(%s, %s) RETURNING id;"
        return scoreboard_address(create, get, set)

    @property
    def __scoreboard_address_params(self) -> scoreboard_address_params:
        create = "CREATE TABLE IF NOT EXISTS scoreboard_address_params("\
                    "id SERIAL PRIMARY KEY, "\
                    "params TEXT NOT NULL, "\
                    "scoreboard_address_id INTEGER REFERENCES scoreboard_address (id));"
        set = "INSERT INTO scoreboard_address_params(scoreboard_address_id, params) VALUES(%s, %s) RETURNING id;"
        return scoreboard_address_params(create, set)

    @property
    def __last_radio_scoreboard_data(self) -> last_radio_scoreboard_data:
        create = "CREATE TABLE IF NOT EXISTS last_scoreboard_data("\
                    "id SERIAL PRIMARY KEY, "\
                    "data TEXT NOT NULL, "\
                    "radio_id INTEGER REFERENCES radio (id));"
        get = "SELECT data FROM last_scoreboard_data "\
                "INNER JOIN radio ON "\
                    "radio.id = last_scoreboard_data.radio_id AND radio.name = %s;"
        set = "INSERT INTO last_scoreboard_data (radio_id, data) "\
                "VALUES ((SELECT id from radio WHERE name = %s), %s) RETURNING id;"
        update = "UPDATE last_scoreboard_data "\
                    "SET data = %s "\
                "WHERE last_scoreboard_data.radio_id = (SELECT id FROM radio WHERE name = %s);"
        delete = "DELETE FROM last_scoreboard_data WHERE radio_id = (SELECT id FROM radio WHERE name = %s);"
        return last_radio_scoreboard_data(create, get, set, update, delete)

    @property
    def __current_radio_scoreboard_data(self) -> current_radio_scoreboard_data:
        create = "CREATE TABLE IF NOT EXISTS current_scoreboard_data("\
                    "id SERIAL PRIMARY KEY, "\
                    "data TEXT NOT NULL, "\
                    "radio_id INTEGER REFERENCES radio (id));"
        get = "SELECT data FROM current_scoreboard_data "\
                "INNER JOIN radio ON "\
                    "radio.id = current_scoreboard_data.radio_id AND radio.name = %s;"
        set = "INSERT INTO current_scoreboard_data (radio_id, data) "\
                "VALUES ((SELECT id from radio WHERE name = %s), %s) RETURNING id;"
        update = "UPDATE current_scoreboard_data "\
                    "SET data = %s "\
                "WHERE current_scoreboard_data.radio_id = (SELECT id FROM radio WHERE name = %s);"
        delete = "DELETE FROM current_scoreboard_data WHERE radio_id = (SELECT id FROM radio WHERE name = %s);"
        return current_radio_scoreboard_data(create, get, set, update, delete)

    @property
    def __radio_activity(self) -> radio_activity:
        create = "CREATE TABLE IF NOT EXISTS radio_activity("\
                    "id SERIAL PRIMARY KEY, "\
                    "radio_name TEXT NOT NULL, "\
                    "guild_id BIGINT NOT NULL, "\
                    "channel_id BIGINT NOT NULL);"
        list = "SELECT radio_name, guild_id, channel_id FROM radio_activity;"
        set = "INSERT INTO radio_activity (radio_name, guild_id, channel_id) VALUES (%s, %s, %s) RETURNING id;"
        delete = "DELETE FROM radio_activity WHERE guild_id = %s;"
        return radio_activity(create, list, set, delete)
    
    @property
    def __silence_group(self) -> silence_group:
        create = "CREATE TABLE IF NOT EXISTS silence_group("\
                    "id SERIAL PRIMARY KEY, "\
                    "guild_id BIGINT NOT NULL);"
        get = "SELECT * FROM silence_group WHERE guild_id = %s;"
        set = "INSERT INTO silence_group(guild_id) VALUES(%s) RETURNING id;"
        delete = "DELETE FROM silence_group WHERE guild_id = %s;"
        return silence_group(create, get, set, delete)