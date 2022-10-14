import sqlite3 as sql
from typing import Any, List, Tuple

from my_types.database import lastrowid, radioActivity, sql_command
from my_types.radio import Station, StationAddress, StationScoreboardAddress

PATH = 'db'
DATABASE = f'{PATH}/DATABASE.db'


class Create_Radio_Tables:
    def __init__(self, db_path: str) -> None:
        with sql.connect(db_path) as connect:
            cursor = connect.cursor()
            cursor.execute(self.radio)
            cursor.execute(self.station_address)
            cursor.execute(self.station_address_params)
            cursor.execute(self.scoreboard_address)
            cursor.execute(self.scoreboard_address_params)
            cursor.execute(self.last_radio_scoreboard_data)
            cursor.execute(self.current_radio_scoreboard_data)
            connect.commit()
            cursor.close

    @property
    def radio(self) -> sql_command:
        cmd =   'CREATE TABLE IF NOT EXISTS radio('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                'name TEXT NOT NULL '\
                ');'
        return cmd

    @property
    def station_address(self) -> sql_command:
        cmd =   'CREATE TABLE IF NOT EXISTS station_address('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                'radio_id INTEGER NOT NULL, '\
                'url TEXT NOT NULL, '\
                'FOREIGN KEY (radio_id) REFERENCES radio(id)'\
                ');'
        return cmd

    @property
    def station_address_params(self) -> sql_command:
        cmd =   'CREATE TABLE IF NOT EXISTS station_address_params('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                'station_address_id INTEGER NOT NULL,'\
                'key TEXT NOT NULL, '\
                'value TEXT NOT NULL, '\
                'FOREIGN KEY (station_address_id) REFERENCES station_address(id)'\
                ');'
        return cmd

    @property
    def scoreboard_address(self) -> sql_command:
        cmd =   'CREATE TABLE IF NOT EXISTS scoreboard_address('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                'radio_id INTEGER NOT NULL,'\
                'url TEXT NOT NULL, '\
                'FOREIGN KEY (radio_id) REFERENCES radio(id)'\
                ');'
        return cmd

    @property
    def scoreboard_address_params(self) -> sql_command:
        cmd =   'CREATE TABLE IF NOT EXISTS scoreboard_address_params('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                'scoreboard_address_id INTEGER NOT NULL,'\
                'key TEXT NOT NULL, '\
                'value TEXT NOT NULL, '\
                'FOREIGN KEY (scoreboard_address_id) REFERENCES scoreboard_address(id)'\
                ');'
        return cmd

    @property
    def last_radio_scoreboard_data(self):
        cmd =   'CREATE TABLE IF NOT EXISTS scoreboard_data('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                'radio_id INTEGER NOT NULL, '\
                'data TEXT NOT NULL, '\
                'FOREIGN KEY (radio_id) REFERENCES radio(id)'\
                ');'
        return cmd
    
    @property
    def current_radio_scoreboard_data(self):
        cmd =   'CREATE TABLE IF NOT EXISTS current_scoreboard_data('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                'radio_id INTEGER NOT NULL, '\
                'data TEXT NOT NULL, '\
                'FOREIGN KEY (radio_id) REFERENCES radio(id)'\
                ');'
        return cmd


class Create_Discord_Activity_Tables:
    def __init__(self, db_path: str) -> None:
        with sql.connect(db_path) as connect:
            cursor = connect.cursor()
            cursor.execute(self.radio_activity)
            connect.commit()
            cursor.close()

    @property
    def radio_activity(self) -> str:
        cmd =   'CREATE TABLE IF NOT EXISTS radio_activity('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
                'radio_name TEXT NOT NULL, '\
                'guild_id INTEGER NOT NULL, '\
                'channel_id INTEGER NOT NULL'\
                ');'
        return cmd


class Connect:
    def __init__(self, db_path: str = DATABASE) -> None:
        self.__db = db_path
        Create_Radio_Tables(self.__db)
        Create_Discord_Activity_Tables(self.__db)
    
    def get_radio_list(self) -> List[str | None]:
        cmd = "SELECT name FROM radio;"
        raw =  self.__execute(cmd, method='fetchall')
        return  self.__normalize_list(raw)
    
    def get_radio_station_address(self, radio_name: str) -> None | StationAddress:
        cmd = "SELECT url, key, value FROM radio "\
                "INNER JOIN station_address ON "\
                    "radio.id = station_address.radio_id AND radio.name = ? "\
                    "INNER JOIN station_address_params ON "\
                        "station_address.id == station_address_params.station_address_id;"
        raw = self.__execute(cmd, (radio_name, ), "fetchall")
        return self.__normalize_radio_address(raw)
    
    def get_radio_scoreboard_address(self, radio_name: str) -> None | StationScoreboardAddress:
        cmd = "SELECT url, key, value FROM radio "\
                "INNER JOIN scoreboard_address ON "\
                    "radio.id = scoreboard_address.radio_id AND radio.name = ? "\
                    "INNER JOIN scoreboard_address_params ON "\
                        "scoreboard_address.id == scoreboard_address_params.scoreboard_address_id;"
        raw =  self.__execute(cmd, (radio_name, ), "fetchall")
        return self.__normalize_radio_scoreboard_address(raw)
    
    def set_radio(self, name: str, url: str, params: dict, scoreboard_url: str = None, scoreboard_params: dict = None) -> None:
        if name in self.get_radio_list():
            raise BaseException(f'Radio "{name}" exists in database')

        cmd = "INSERT INTO radio(name) VALUES(?);"
        radio_id = self.__execute(cmd, (name,), 'lastrowid')
        
        radio_address_id = self.__set_radio_address(radio_id, url)
        self.__set_radio_address_params(radio_address_id, params)
        
        if scoreboard_url is not None:
            scoreboard_id = self.__set_radio_scoreboard_address(radio_id, scoreboard_url)
        
        if None not in (scoreboard_url, scoreboard_params):
            self.__set_radio_scoreboard_address_params(scoreboard_id, scoreboard_params)

    def get_radio(self, radio_name: str) -> Station:
        if radio_name not in self.get_radio_list():
            raise BaseException(f'Radio "{radio_name}" is not exists in database')
        station_address = self.get_radio_station_address(radio_name)
        scoreboard_address = self.get_radio_scoreboard_address(radio_name)
        data = Station(
            name=radio_name,
            station_address=station_address,
            scoreboard_address=scoreboard_address
        )
        return data
    
    def set_radio_activity(self, guild_id: int, channel_id: int, radio_name: str) -> None:
        cmd = "INSERT INTO radio_activity (radio_name, guild_id, channel_id) VALUES (?, ?, ?);"
        self.__execute(cmd, (radio_name, guild_id, channel_id))

    def delete_radio_activity(self, guild_id: int) -> None:
        cmd = "DELETE FROM radio_activity WHERE guild_id = ?;"
        self.__execute(cmd, (guild_id,))

    def get_radio_activity(self) -> List[radioActivity] | None:
        cmd = "SELECT radio_name, guild_id, channel_id FROM radio_activity;"
        raw = self.__execute(cmd, method='fetchall')
        return self.__normalize_radio_activity(raw)

    def get_last_scoreboard(self, radio_name: str) -> str | None:
        cmd = "SELECT data FROM scoreboard_data "\
                "INNER JOIN radio ON "\
                    "radio.id = scoreboard_data.radio_id AND radio.name = ?;"
        raw = self.__execute(cmd, (radio_name,), 'fetchone')
        if raw is None:
            return None
        return raw[0]

    def set_last_scoreboard(self, radio_name: str, data: str) -> None:
        cmd =   "INSERT INTO scoreboard_data (data, radio_id) "\
                "VALUES (?, (SELECT id from radio WHERE name = ?));"
        self.__execute(cmd, (data, radio_name))

    def update_last_scoreboard(self, radio_name: str, data: str) -> None:
        cmd =   "UPDATE scoreboard_data "\
                    "SET data = ? "\
                "WHERE scoreboard_data.radio_id = (SELECT id FROM radio WHERE name = ?);"
        self.__execute(cmd, (data, radio_name))

    def delete_last_scoreboard(self, radio_name: str) -> None:
        cmd = "DELETE FROM scoreboard_data WHERE radio_id = (SELECT id FROM radio WHERE name = ?);"
        self.__execute(cmd, (radio_name,))

    def get_current_scoreboard(self, radio_name: str) -> str | None:
        cmd = "SELECT data FROM current_scoreboard_data "\
                "INNER JOIN radio ON "\
                    "radio.id = current_scoreboard_data.radio_id AND radio.name = ?;"
        raw = self.__execute(cmd, (radio_name,), 'fetchone')
        if raw is None:
            return None
        return raw[0]

    def set_current_scoreboard(self, radio_name: str, data: str) -> None:
        cmd =   "INSERT INTO current_scoreboard_data (data, radio_id) "\
                "VALUES (?, (SELECT id from radio WHERE name = ?));"
        self.__execute(cmd, (data, radio_name))

    def update_current_scoreboard(self, radio_name: str, data: str) -> None:
        cmd =   "UPDATE current_scoreboard_data "\
                    "SET data = ? "\
                "WHERE current_scoreboard_data.radio_id = (SELECT id FROM radio WHERE name = ?);"
        self.__execute(cmd, (data, radio_name))

    def delete_current_scoreboard(self, radio_name: str) -> None:
        cmd = "DELETE FROM current_scoreboard_data WHERE radio_id = (SELECT id FROM radio WHERE name = ?);"
        self.__execute(cmd, (radio_name,))

    def __normalize_radio_activity(self, raw: List[Tuple[str | int]]) -> List[radioActivity] | None:
        if not raw:
            return None
        
        data = []
        for activity in raw:
            data.append(radioActivity(*activity))
        return data

    def __normalize_list(self, data: List[Tuple[str]]) -> List[str]:
        return [x[0] for x in data]

    def __normalize_radio_address(self, data: Tuple[Tuple[str]]) -> StationAddress:
        if len(data) < 1:
            return StationAddress('', {})
        params = {}
        url = data[0][0]
        for el in data:
            params[el[1]] = el[2]
        return StationAddress(url, params)

    def __normalize_radio_scoreboard_address(self, data: Tuple[Tuple[str]]) -> StationScoreboardAddress | None:
        if len(data) < 1:
            return None
        params = {}
        url = data[0][0]
        for el in data:
            params[el[1]] = el[2]
        return StationScoreboardAddress(url, params)

    def __set_radio_address(self, radio_id: int, url: str) -> lastrowid:
        cmd = "INSERT INTO station_address(radio_id, url) VALUES(?, ?);"
        return self.__execute(cmd, (radio_id, url), 'lastrowid')

    def __set_radio_address_params(self, radio_address_id: int, params: dict) -> None:
        cmd = "INSERT INTO station_address_params(station_address_id, key, value) VALUES(?, ?, ?);"
        for key, value in params.items():
            self.__execute(cmd, (radio_address_id, key, value))
    
    def __set_radio_scoreboard_address(self, radio_id: int, url: str) -> lastrowid:
        cmd = "INSERT INTO scoreboard_address(radio_id, url) VALUES(?, ?);"
        return self.__execute(cmd, (radio_id, url), 'lastrowid')
    
    def __set_radio_scoreboard_address_params(self, scoreboard_id: int, params: dict) -> None:
        cmd  = "INSERT INTO scoreboard_address_params(scoreboard_address_id, key, value) VALUES(?, ?, ?);"
        for key, value in params.items():
            self.__execute(cmd, (scoreboard_id, key, value))
    
    def __execute(self, cmd: sql_command, data: tuple = None, method: str = None) -> Any:
        result = ''
        with sql.connect(self.__db) as connect:
            cursor = connect.cursor()
            if data:
                cursor.execute(cmd, data)
            else:
                cursor.execute(cmd)

            match method:
                case "fetchone":
                    result = cursor.fetchone()
                case "fetchall":
                    result = cursor.fetchall()
                case "lastrowid":
                    result = cursor.lastrowid
            cursor.close
        return result
