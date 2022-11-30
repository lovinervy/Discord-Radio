from typing import List, Tuple
import sqlite3
import psycopg2

from my_types.database import Engine
from my_types.database import sql_command
from my_types.database import (
    Tables,
    RadioTable,
    StationAddressTable,
    StationAddressParamsTable,
    ScoreboardAddressTable,
    ScoreboardAddressParamsTable,
    LastRadioScoreboardDataTable,
    CurrentRadioScoreboardDataTable,
    RadioActivityTable,
    SilenceGroupTable,
)


PATH = 'db'
DATABASE = f'{PATH}/DATABASE.db'


class SQLite(Engine):   # pylint: disable=too-few-public-methods
    """Engine class for configure tables into SQLite database, set up SQL-commands"""

    def __init__(self, db_path: str = DATABASE) -> None:
        super().__init__()
        self.__path = db_path

        self.tables = Tables(
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

    def execute(self, cmd: sql_command, data: tuple = (), method: str = "") \
            -> int | Tuple | List | None:
        with sqlite3.connect(self.__path) as connect:
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
    def __radio(self) -> RadioTable:
        create: sql_command = 'CREATE TABLE IF NOT EXISTS radio('\
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
            'name TEXT NOT NULL);'
        all_data: sql_command = 'SELECT name FROM radio;'
        insert: sql_command = 'INSERT INTO radio(name) VALUES(?);'
        return RadioTable(create, all_data, insert)

    @property
    def __station_address(self) -> StationAddressTable:
        create = 'CREATE TABLE IF NOT EXISTS station_address('\
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
            'radio_id INTEGER NOT NULL, '\
            'url TEXT NOT NULL, '\
            'FOREIGN KEY (radio_id) REFERENCES radio(id));'
        insert = "INSERT INTO station_address(radio_id, url) VALUES(?, ?);"
        get = "SELECT url, params FROM radio "\
            "INNER JOIN station_address ON "\
            "radio.id = station_address.radio_id AND radio.name = ? "\
            "INNER JOIN station_address_params ON "\
            "station_address.id = station_address_params.station_address_id;"
        return StationAddressTable(create, get, insert)

    @property
    def __station_address_params(self) -> StationAddressParamsTable:
        create = 'CREATE TABLE IF NOT EXISTS station_address_params('\
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
            'station_address_id INTEGER NOT NULL,'\
            'params TEXT NOT NULL, '\
            'FOREIGN KEY (station_address_id) REFERENCES station_address(id));'
        insert = "INSERT INTO station_address_params(station_address_id, params) VALUES(?, ?);"
        return StationAddressParamsTable(create, insert)

    @property
    def __scoreboard_address(self) -> ScoreboardAddressTable:
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
        insert = "INSERT INTO scoreboard_address(radio_id, url) VALUES(?, ?);"
        return ScoreboardAddressTable(create, get, insert)

    @property
    def __scoreboard_address_params(self) -> ScoreboardAddressParamsTable:
        create = 'CREATE TABLE IF NOT EXISTS scoreboard_address_params('\
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
            'scoreboard_address_id INTEGER NOT NULL,'\
            'params TEXT NOT NULL, '\
            'FOREIGN KEY (scoreboard_address_id) REFERENCES scoreboard_address(id));'
        insert = "INSERT INTO scoreboard_address_params(scoreboard_address_id, params) "\
            "VALUES(?, ?);"
        return ScoreboardAddressParamsTable(create, insert)

    @property
    def __last_radio_scoreboard_data(self) -> LastRadioScoreboardDataTable:
        create = 'CREATE TABLE IF NOT EXISTS last_scoreboard_data('\
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
            'radio_id INTEGER NOT NULL, '\
            'data TEXT NOT NULL, '\
            'FOREIGN KEY (radio_id) REFERENCES radio(id));'
        get = "SELECT data FROM last_scoreboard_data "\
            "INNER JOIN radio ON "\
            "radio.id = last_scoreboard_data.radio_id AND radio.name = ?;"
        insert = "INSERT INTO last_scoreboard_data (radio_id, data) "\
            "VALUES ((SELECT id from radio WHERE name = ?), ?);"
        update = "UPDATE last_scoreboard_data "\
            "SET data = ? "\
            "WHERE last_scoreboard_data.radio_id = (SELECT id FROM radio WHERE name = ?);"
        delete = "DELETE FROM last_scoreboard_data WHERE "\
            "radio_id = (SELECT id FROM radio WHERE name = ?);"
        return LastRadioScoreboardDataTable(create, get, insert, update, delete)

    @property
    def __current_radio_scoreboard_data(self) -> CurrentRadioScoreboardDataTable:
        create = 'CREATE TABLE IF NOT EXISTS current_scoreboard_data('\
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
            'radio_id INTEGER NOT NULL, '\
            'data TEXT NOT NULL, '\
            'FOREIGN KEY (radio_id) REFERENCES radio(id));'
        get = "SELECT data FROM current_scoreboard_data "\
            "INNER JOIN radio ON "\
            "radio.id = current_scoreboard_data.radio_id AND radio.name = ?;"
        insert = "INSERT INTO current_scoreboard_data (radio_id, data) "\
            "VALUES ((SELECT id from radio WHERE name = ?), ?);"
        update = "UPDATE current_scoreboard_data "\
            "SET data = ? "\
            "WHERE current_scoreboard_data.radio_id = (SELECT id FROM radio WHERE name = ?);"
        delete = "DELETE FROM current_scoreboard_data WHERE "\
            "radio_id = (SELECT id FROM radio WHERE name = ?);"
        return CurrentRadioScoreboardDataTable(create, get, insert, update, delete)

    @property
    def __radio_activity(self) -> RadioActivityTable:
        create = 'CREATE TABLE IF NOT EXISTS radio_activity('\
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
            'radio_name TEXT NOT NULL, '\
            'guild_id INTEGER NOT NULL, '\
            'channel_id INTEGER NOT NULL);'
        all_data = "SELECT radio_name, guild_id, channel_id FROM radio_activity;"
        insert = "INSERT INTO radio_activity (radio_name, guild_id, channel_id) VALUES (?, ?, ?);"
        delete = "DELETE FROM radio_activity WHERE guild_id = ?;"
        return RadioActivityTable(create, all_data, insert, delete)

    @property
    def __silence_group(self) -> SilenceGroupTable:
        create = 'CREATE TABLE IF NOT EXISTS silence_group('\
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
            'guild_id INTEGER NOT NULL);'
        get = "SELECT * FROM silence_group WHERE guild_id = ?;"
        insert = "INSERT INTO silence_group(guild_id) VALUES(?);"
        delete = "DELETE FROM silence_group WHERE guild_id = ?;"
        return SilenceGroupTable(create, get, insert, delete)


class PostgreSQL(Engine):   # pylint: disable=too-few-public-methods
    """Engine class for init connection with PostgreSQL, configure tables, set up SQL-commands"""

    def __init__(self, user: str, password: str, host: str, port: int) -> None:
        super().__init__()
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port

        self.__connect()

        self.tables = Tables(
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
        self._connect = psycopg2.connect(
            f"user='{self.__user}' host='{self.__host}' "
            f"password='{self.__password}' port='{self.__port}'")

    def execute(self, cmd: sql_command, data: tuple = None, method: str = None) \
            -> int | Tuple | List | None:
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
            self._connect.commit()
            cursor.close()
            return None

        except psycopg2.OperationalError:
            print("Error:", cmd, data, method)
            return None

    @property
    def __radio(self) -> RadioTable:
        create = "CREATE TABLE IF NOT EXISTS radio("\
            "id SERIAL PRIMARY KEY, "\
            "name TEXT NOT NULL);"
        all_data = "SELECT name FROM radio;"
        insert = "INSERT INTO radio (name) VALUES (%s) RETURNING id;"
        return RadioTable(create, all_data, insert)

    @property
    def __station_address(self) -> StationAddressTable:
        create = "CREATE TABLE IF NOT EXISTS station_address("\
            "id SERIAL PRIMARY KEY, "\
            "url TEXT NOT NULL, "\
            "radio_id INTEGER NOT NULL, "\
            "FOREIGN KEY(radio_id) REFERENCES radio(id));"
        insert = "INSERT INTO station_address (radio_id, url) VALUES (%s, %s) RETURNING id;"
        get = "SELECT url, params FROM radio "\
            "INNER JOIN station_address ON "\
            "radio.id = station_address.radio_id AND radio.name = %s "\
            "INNER JOIN station_address_params ON "\
            "station_address.id = station_address_params.station_address_id;"
        return StationAddressTable(create, get, insert)

    @property
    def __station_address_params(self) -> StationAddressParamsTable:
        create = "CREATE TABLE IF NOT EXISTS station_address_params("\
            "id SERIAL PRIMARY KEY, "\
            "params TEXT NOT NULL, "\
            "station_address_id INTEGER REFERENCES station_address (id));"
        insert = "INSERT INTO station_address_params(station_address_id, params) "\
            "VALUES(%s, %s) RETURNING id;"
        return StationAddressParamsTable(create, insert)

    @property
    def __scoreboard_address(self) -> ScoreboardAddressTable:
        create = "CREATE TABLE IF NOT EXISTS scoreboard_address("\
            "id SERIAL PRIMARY KEY, "\
            "url TEXT NOT NULL, "\
            "radio_id INTEGER REFERENCES radio (id));"
        get = "SELECT url, params FROM radio "\
            "INNER JOIN scoreboard_address ON "\
            "radio.id = scoreboard_address.radio_id AND radio.name = %s "\
            "INNER JOIN scoreboard_address_params ON "\
            "scoreboard_address.id = scoreboard_address_params.scoreboard_address_id;"
        insert = "INSERT INTO scoreboard_address(radio_id, url) VALUES(%s, %s) RETURNING id;"
        return ScoreboardAddressTable(create, get, insert)

    @property
    def __scoreboard_address_params(self) -> ScoreboardAddressParamsTable:
        create = "CREATE TABLE IF NOT EXISTS scoreboard_address_params("\
            "id SERIAL PRIMARY KEY, "\
            "params TEXT NOT NULL, "\
            "scoreboard_address_id INTEGER REFERENCES scoreboard_address (id));"
        insert = "INSERT INTO scoreboard_address_params(scoreboard_address_id, params) "\
            "VALUES(%s, %s) RETURNING id;"
        return ScoreboardAddressParamsTable(create, insert)

    @property
    def __last_radio_scoreboard_data(self) -> LastRadioScoreboardDataTable:
        create = "CREATE TABLE IF NOT EXISTS last_scoreboard_data("\
            "id SERIAL PRIMARY KEY, "\
            "data TEXT NOT NULL, "\
            "radio_id INTEGER REFERENCES radio (id));"
        get = "SELECT data FROM last_scoreboard_data "\
            "INNER JOIN radio ON "\
            "radio.id = last_scoreboard_data.radio_id AND radio.name = %s;"
        insert = "INSERT INTO last_scoreboard_data (radio_id, data) "\
            "VALUES ((SELECT id from radio WHERE name = %s), %s) RETURNING id;"
        update = "UPDATE last_scoreboard_data "\
            "SET data = %s "\
            "WHERE last_scoreboard_data.radio_id = (SELECT id FROM radio WHERE name = %s);"
        delete = "DELETE FROM last_scoreboard_data WHERE "\
            "radio_id = (SELECT id FROM radio WHERE name = %s);"
        return LastRadioScoreboardDataTable(create, get, insert, update, delete)

    @property
    def __current_radio_scoreboard_data(self) -> CurrentRadioScoreboardDataTable:
        create = "CREATE TABLE IF NOT EXISTS current_scoreboard_data("\
            "id SERIAL PRIMARY KEY, "\
            "data TEXT NOT NULL, "\
            "radio_id INTEGER REFERENCES radio (id));"
        get = "SELECT data FROM current_scoreboard_data "\
            "INNER JOIN radio ON "\
            "radio.id = current_scoreboard_data.radio_id AND radio.name = %s;"
        insert = "INSERT INTO current_scoreboard_data (radio_id, data) "\
            "VALUES ((SELECT id from radio WHERE name = %s), %s) RETURNING id;"
        update = "UPDATE current_scoreboard_data "\
            "SET data = %s "\
            "WHERE current_scoreboard_data.radio_id = "\
            "(SELECT id FROM radio WHERE name = %s);"
        delete = "DELETE FROM current_scoreboard_data WHERE "\
            "radio_id = (SELECT id FROM radio WHERE name = %s);"
        return CurrentRadioScoreboardDataTable(create, get, insert, update, delete)

    @property
    def __radio_activity(self) -> RadioActivityTable:
        create = "CREATE TABLE IF NOT EXISTS radio_activity("\
            "id SERIAL PRIMARY KEY, "\
            "radio_name TEXT NOT NULL, "\
            "guild_id BIGINT NOT NULL, "\
            "channel_id BIGINT NOT NULL);"
        all_data = "SELECT radio_name, guild_id, channel_id FROM radio_activity;"
        insert = "INSERT INTO radio_activity (radio_name, guild_id, channel_id) "\
            "VALUES (%s, %s, %s) RETURNING id;"
        delete = "DELETE FROM radio_activity WHERE guild_id = %s;"
        return RadioActivityTable(create, all_data, insert, delete)

    @property
    def __silence_group(self) -> SilenceGroupTable:
        create = "CREATE TABLE IF NOT EXISTS silence_group("\
            "id SERIAL PRIMARY KEY, "\
            "guild_id BIGINT NOT NULL);"
        get = "SELECT * FROM silence_group WHERE guild_id = %s;"
        insert = "INSERT INTO silence_group(guild_id) VALUES(%s) RETURNING id;"
        delete = "DELETE FROM silence_group WHERE guild_id = %s;"
        return SilenceGroupTable(create, get, insert, delete)
