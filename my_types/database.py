from dataclasses import dataclass
from typing import List, Tuple, TypeAlias, Any
from abc import ABC, abstractmethod
from my_types.radio import StationAddress, StationScoreboardAddress, Station


@dataclass
class RadioActivity:
    """Struct for storing info about activity in "discord" channel"""
    radio: str
    guild_id: int
    channel_id: int


sql_command: TypeAlias = str
lastrowid: TypeAlias = int


class Connector(ABC):
    """Abstract Connector class for show need methods and hinting"""
    @abstractmethod
    def get_radio_list(self) -> List[str | None]:
        """Get all data from radio table"""

    @abstractmethod
    def get_radio_station_address(self, radio_name: str) -> None | StationAddress:
        """Get data from station address table"""

    @abstractmethod
    def get_radio_scoreboard_address(self, radio_name: str) -> None | StationScoreboardAddress:
        """Get data from scoreboard address table"""

    @abstractmethod
    def set_radio(self, name: str, url: str, params: dict, scoreboard_url: str = None,\
        scoreboard_params: dict = None) -> None:    # pylint: disable=too-many-arguments
        """Insert data into radio and scoreboard table"""

    @abstractmethod
    def get_radio(self, radio_name: str) -> Station:
        """Get data from radio table"""

    @abstractmethod
    def set_radio_activity(self, guild_id: int, channel_id: int, radio_name: str) -> None:
        """Insert data into radio activity table"""

    @abstractmethod
    def delete_radio_activity(self, guild_id: int) -> None:
        """Delete data from radio activity table"""

    @abstractmethod
    def get_radio_activity(self) -> List[RadioActivity] | None:
        """Get all data from radio activity table"""

    @abstractmethod
    def get_last_scoreboard(self, radio_name: str) -> str | None:
        """Get data from last scoreboard table"""

    @abstractmethod
    def set_last_scoreboard(self, radio_name: str, data: str) -> None:
        """Insert data into last scoreboard table"""

    @abstractmethod
    def update_last_scoreboard(self, radio_name: str, data: str) -> None:
        """Update data in last scoreboard table"""

    @abstractmethod
    def delete_last_scoreboard(self, radio_name: str) -> None:
        """Delete data from last scoreboard table"""

    @abstractmethod
    def get_current_scoreboard(self, radio_name: str) -> str | None:
        """Get data from current scoreboard"""

    @abstractmethod
    def set_current_scoreboard(self, radio_name: str, data: str) -> None:
        """Insert data into current scoreboard table"""

    @abstractmethod
    def update_current_scoreboard(self, radio_name: str, data: str) -> None:
        """Update radio_name row in current scoreboard table"""

    @abstractmethod
    def delete_current_scoreboard(self, radio_name: str) -> None:
        """Delete radio_name row from current scoreboard table"""

    @abstractmethod
    def get_from_silence_group(self, guild_id: int) -> Tuple[int]:
        """Get (id, guild_id) from silence group table"""

    @abstractmethod
    def delete_from_silence_group(self, guild_id: int) -> None:
        """Delete guild id into silence group table"""

    @abstractmethod
    def add_in_silence_group(self, guild_id: int) -> None:
        """Insert guild id into silence group table"""


@dataclass
class RadioTable:
    """Raw commands struct for work with radio table"""
    create: sql_command
    list: sql_command
    set: sql_command


@dataclass
class StationAddressTable:
    """Raw commands struct for work with station_address table"""
    create: sql_command
    get: sql_command
    set: sql_command


@dataclass
class StationAddressParamsTable:
    """Raw commands struct for work with station_address_params table"""
    create: sql_command
    set: sql_command


@dataclass
class ScoreboardAddressTable:
    """Raw commands struct for work with scoreboard_address table"""
    create: sql_command
    get: sql_command
    set: sql_command


@dataclass
class ScoreboardAddressParamsTable:
    """Raw commands struct for work with scoreboard_address_params table"""
    create: sql_command
    set: sql_command


@dataclass
class LastRadioScoreboardDataTable:
    """Raw commands struct for work with last_scoreboard_data table"""
    create: sql_command
    get: sql_command
    set: sql_command
    update: sql_command
    delete: sql_command


@dataclass
class CurrentRadioScoreboardDataTable:
    """Raw commands struct for work with current_scoreboard_data table"""
    create: sql_command
    get: sql_command
    set: sql_command
    update: sql_command
    delete: sql_command


@dataclass
class RadioActivityTable:
    """Raw commands struct for work with radio_activity table"""
    create: sql_command
    list: sql_command
    set: sql_command
    delete: sql_command


@dataclass
class SilenceGroupTable:
    """Raw commands struct for work with silence_group table"""
    create: sql_command
    get: sql_command
    set: sql_command
    delete: sql_command


@dataclass
class Tables:   # pylint: disable=too-many-instance-attributes
    """Struct for works with raw commands in database"""
    radio: RadioTable
    station_address: StationAddressTable
    station_address_params: StationAddressParamsTable
    scoreboard_address: ScoreboardAddressTable
    scoreboard_address_params: ScoreboardAddressParamsTable
    last_radio_scoreboard_data: LastRadioScoreboardDataTable
    current_radio_scoreboard_data: CurrentRadioScoreboardDataTable
    radio_activity: RadioActivityTable
    silence_group: SilenceGroupTable


class Engine(ABC):  # pylint: disable=too-few-public-methods
    """Engine class view for working with raw SQL command"""

    def __init__(self) -> None:
        self.tables: Tables = None

    @abstractmethod
    def execute(self, cmd: sql_command, data: tuple = None, method: str = None) -> Any | None:
        """
        Command executor:
        cmd: sql command get from Engine.tables...
        data: Any | None
        method: str set method as "fetchone", "fetchall", "lastrowid", "commit"
        """
