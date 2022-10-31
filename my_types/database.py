from ast import Str
from dataclasses import dataclass
from typing import List, Tuple, TypeAlias, Any
from abc import ABC, abstractmethod
from my_types.radio import StationAddress, StationScoreboardAddress, Station


@dataclass
class radioActivity:
    radio: str
    guild_id: int
    channel_id: int

sql_command: TypeAlias = str
lastrowid: TypeAlias = int


class Connector(ABC):
    @abstractmethod
    def get_radio_list(self) -> List[str | None]:
        pass

    @abstractmethod
    def get_radio_station_address(self, radio_name: str) -> None | StationAddress:
        pass

    @abstractmethod
    def get_radio_scoreboard_address(self, radio_name: str) -> None | StationScoreboardAddress:
        pass

    @abstractmethod
    def set_radio(self, name: str, url: str, params: dict, scoreboard_url: str = None, scoreboard_params: dict = None) -> None:
        pass

    @abstractmethod
    def get_radio(self, radio_name: str) -> Station:
        pass

    @abstractmethod
    def set_radio_activity(self, guild_id: int, channel_id: int, radio_name: str) -> None:
        pass

    @abstractmethod
    def delete_radio_activity(self, guild_id: int) -> None:
        pass

    @abstractmethod
    def get_radio_activity(self) -> List[radioActivity] | None:
        pass

    @abstractmethod
    def get_last_scoreboard(self, radio_name: str) -> str | None:
        pass

    @abstractmethod
    def set_last_scoreboard(self, radio_name: str, data: str) -> None:
        pass

    @abstractmethod
    def update_last_scoreboard(self, radio_name: str, data: str) -> None:
        pass

    @abstractmethod
    def delete_last_scoreboard(self, radio_name: str) -> None:
        pass

    @abstractmethod
    def get_current_scoreboard(self, radio_name: str) -> str | None:
        pass

    @abstractmethod
    def set_current_scoreboard(self, radio_name: str, data: str) -> None:
        pass

    @abstractmethod
    def update_current_scoreboard(self, radio_name: str, data: str) -> None:
        pass

    @abstractmethod
    def delete_current_scoreboard(self, radio_name: str) -> None:
        pass

    @abstractmethod
    def get_from_silence_group(self, guild_id: int) -> Tuple[int]:
        pass

    @abstractmethod
    def delete_from_silence_group(self, guild_id: int) -> None:
        pass

    @abstractmethod
    def add_in_silence_group(self, guild_id: int) -> None:
        pass


@dataclass
class radio:
    create: str 
    list: str
    set: Str


@dataclass
class station_address:
    create: str
    get: str
    set: str


@dataclass
class station_address_params:
    create: str
    set: str


@dataclass
class scoreboard_address:
    create: str
    get: str
    set: str


@dataclass
class scoreboard_address_params:
    create: str
    set: str


@dataclass
class last_radio_scoreboard_data:
    create: str
    get: str
    set: str
    update: str
    delete: str


@dataclass
class current_radio_scoreboard_data:
    create: str
    get: str
    set: str
    update: str
    delete: str


@dataclass
class radio_activity:
    create: str
    list: str
    set: str
    delete: str


@dataclass
class silence_group:
    create: str
    get: str
    set: str
    delete: str


@dataclass
class tables:
    radio: radio
    station_address: station_address
    station_address_params: station_address_params
    scoreboard_address: scoreboard_address
    scoreboard_address_params: scoreboard_address_params
    last_radio_scoreboard_data: last_radio_scoreboard_data
    current_radio_scoreboard_data: current_radio_scoreboard_data
    radio_activity: radio_activity
    silence_group: silence_group



class Engine(ABC):
    def __init__(self) -> None:
        self.tables: tables = None
    
    @abstractmethod
    def execute(self, cmd: sql_command, data: tuple = None, method: str = None) -> Any | None:
        pass