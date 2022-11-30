import ast

from typing import Any, List, Tuple
from my_types.database import Connector, Engine, RadioActivity
from my_types.radio import (
    Station,
    StationAddress,
    StationScoreboardAddress
)


class Connect(Connector):
    """API for working between SQL Engine and Discord Bot"""

    def __init__(self, engine: Engine) -> None:
        self.tables = engine.tables
        self.execute = engine.execute

        self.__create_tables()

    def __create_tables(self):
        self.execute(self.tables.radio.create, method="commit")
        self.execute(self.tables.station_address.create, method="commit")
        self.execute(self.tables.station_address_params.create,
                     method="commit")
        self.execute(self.tables.scoreboard_address.create, method="commit")
        self.execute(self.tables.scoreboard_address_params.create,
                     method="commit")
        self.execute(
            self.tables.last_radio_scoreboard_data.create, method="commit")
        self.execute(
            self.tables.current_radio_scoreboard_data.create, method="commit")
        self.execute(self.tables.radio_activity.create, method="commit")
        self.execute(self.tables.silence_group.create, method="commit")

    def get_radio_list(self) -> List[str | None]:
        raw = self.execute(self.tables.radio.list, method="fetchall")
        return self.__normalize_list(raw)

    def get_radio_station_address(self, radio_name: str) -> None | StationAddress:
        raw = self.execute(self.tables.station_address.get,
                           (radio_name,), "fetchone")
        return self.__normalize_station_address(raw)

    def get_radio_scoreboard_address(self, radio_name: str) -> None | StationScoreboardAddress:
        raw = self.execute(self.tables.scoreboard_address.get,
                           (radio_name,), "fetchone")
        return self.__normalize_scoreboard_address(raw)

    def set_radio(self, name: str, url: str, params: dict,  # pylint: disable=too-many-arguments
                  scoreboard_url: str = None, scoreboard_params: dict = None) -> None:
        if name in self.get_radio_list():
            raise BaseException(f'Radio "{name}" exists in database')

        radio_id: int = self.execute(
            self.tables.radio.set, (name,), "lastrowid")
        address_id: int = self.execute(
            self.tables.station_address.set, (radio_id, url), "lastrowid")

        self.execute(self.tables.station_address_params.set,
                     (address_id, str(params)))

        if scoreboard_url is not None:
            scoreboard_id: int = self.execute(
                self.tables.scoreboard_address.set, (radio_id, scoreboard_url), "lastrowid")
            if scoreboard_params:
                self.execute(self.tables.scoreboard_address_params.set,
                             (scoreboard_id, str(scoreboard_params)))

    def get_radio(self, radio_name: str) -> Station:
        if radio_name not in self.get_radio_list():
            raise BaseException(
                f'Radio "{radio_name}" is not exists in database')
        station = self.get_radio_station_address(radio_name)
        scoreboard = self.get_radio_scoreboard_address(radio_name)
        return Station(radio_name, station, scoreboard)

    def set_radio_activity(self, guild_id: int, channel_id: int, radio_name: str) -> None:
        self.execute(self.tables.radio_activity.set,
                     (radio_name, guild_id, channel_id))

    def delete_radio_activity(self, guild_id: int) -> None:
        self.execute(self.tables.radio_activity.delete, (guild_id,))

    def get_radio_activity(self) -> List[RadioActivity] | None:
        raw = self.execute(self.tables.radio_activity.list, method="fetchall")
        return self.__normalize_radio_activity(raw)

    def get_last_scoreboard(self, radio_name: str) -> str | None:
        raw = self.execute(
            self.tables.last_radio_scoreboard_data.get, (radio_name,), "fetchone")
        if raw is None:
            return None
        return raw[0]

    def set_last_scoreboard(self, radio_name: str, data: str) -> None:
        self.execute(self.tables.last_radio_scoreboard_data.set,
                     (radio_name, data))

    def update_last_scoreboard(self, radio_name: str, data: str) -> None:
        self.execute(self.tables.last_radio_scoreboard_data.update,
                     (data, radio_name))

    def delete_last_scoreboard(self, radio_name: str) -> None:
        self.execute(
            self.tables.last_radio_scoreboard_data.delete, (radio_name,))

    def get_current_scoreboard(self, radio_name: str) -> str | None:
        raw = self.execute(
            self.tables.current_radio_scoreboard_data.get, (radio_name,), "fetchone")
        if raw is None:
            return None
        return raw[0]

    def set_current_scoreboard(self, radio_name: str, data: str) -> None:
        self.execute(self.tables.current_radio_scoreboard_data.set,
                     (radio_name, data))

    def update_current_scoreboard(self, radio_name: str, data: str) -> None:
        self.execute(
            self.tables.current_radio_scoreboard_data.update, (data, radio_name))

    def delete_current_scoreboard(self, radio_name: str) -> None:
        self.execute(
            self.tables.current_radio_scoreboard_data.delete, (radio_name,))

    def get_from_silence_group(self, guild_id: int) -> Tuple[int]:
        return self.execute(self.tables.silence_group.get, (guild_id,), "fetchone")

    def delete_from_silence_group(self, guild_id: int) -> None:
        self.execute(self.tables.silence_group.delete, (guild_id,))

    def add_in_silence_group(self, guild_id: int) -> None:
        self.execute(self.tables.silence_group.set, (guild_id,))

    def __normalize_list(self, data: List[Tuple[Any]]) -> List[str]:
        return [x[0] for x in data]

    def __normalize_station_address(self, data: Tuple[str]) -> StationAddress:
        if not data:
            return StationAddress("", {})
        url = data[0]
        params = ast.literal_eval(data[1])
        return StationAddress(url, params)

    def __normalize_scoreboard_address(self, data: Tuple[str]) -> StationScoreboardAddress | None:
        if not data:
            return None
        url = data[0]
        params = ast.literal_eval(data[1])
        return StationScoreboardAddress(url, params)

    def __normalize_radio_activity(self, data: List[Tuple[str | int]]) -> List[RadioActivity]:
        if not data:
            return None
        activity_list = []
        for activity in data:
            activity_list.append(RadioActivity(*activity))
        return activity_list
