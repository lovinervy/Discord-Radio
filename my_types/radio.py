from dataclasses import dataclass


@dataclass
class StationAddress:
    """Station address struct"""
    url: str
    params: dict


@dataclass
class StationScoreboardAddress:
    """Station scoreboard address struct"""
    url: str
    params: dict


@dataclass
class Station:
    """Station struct"""
    name: str
    station_address: StationAddress
    scoreboard_address: StationScoreboardAddress


@dataclass
class MusicInfo:
    """
    Music info struct
    """
    artist: str = None
    title: str = None
    year: str = None
    duration: str = None
    composer: str = None

    @property
    def __formatted_text(self):
        text = f"Music: {self.artist} - {self.title}\n"\
            f"Year: {self.year}\n"\
            f"Duration: {self.duration}\n"\
            f"Composer: {self.composer}"
        return text

    def __repr__(self) -> str:
        return self.__formatted_text
