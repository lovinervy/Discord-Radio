from dataclasses import dataclass
import time
import json
import aiohttp


@dataclass
class StationAddress:
    url: str
    params: dict


@dataclass
class StationScoreboardAddress:
    url: str
    params: dict


@dataclass
class Station:
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

    def to_str(self):
        return self.__str__()    

    def __str__(self) -> str:
        return self.__formatted_text

    def __repr__(self) -> str:
        return self.__formatted_text


def wtf_time_to_std_time(wtf_time: str = None) -> str:
    '''
    Get wtf_time type(str) as "PT0M00.000S"
    return type(str) as hh:mm:ss.ms as "00:00:00.000"
    '''
    if not wtf_time:
        return

    minute = wtf_time[2: wtf_time.find('M')]
    seconds = wtf_time[wtf_time.find('M') + 1: -1]

    if len(minute) == 1:
        minute = f'0{minute}'
    elif len(minute) == 0:
        minute == '00'
    elif len(minute) > 2:
        return '00:00:00.000'

    if seconds.find('.') == 1:
        seconds = f'0{seconds}'
    return f'00:{minute}:{seconds}'


def __update_time_in_scoreboard(scoreboard: StationScoreboardAddress) -> StationScoreboardAddress:
    scoreboard.params['_'] = str(int(time.time() // 1))
    return scoreboard


async def __request_get(url: str, params: dict):
    with open('headers.json', 'r') as f:
        headers = json.load(f)
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params, headers=headers) as response:
            if response.status == 200:
                data = await response.text()
    return data


async def what_plays_on_asiadreamradio(scoreboard: StationScoreboardAddress) -> MusicInfo | None:
    __update_time_in_scoreboard(scoreboard)
    response = await __request_get(scoreboard.url, scoreboard.params)
    content: dict = json.loads(response)
    info = content.get('m_Item2')
    if info:
        return MusicInfo(
            artist = info.get('Artist'),
            title = info.get('Title'),
            year = info.get('Year'),
            duration = wtf_time_to_std_time(info.get('Duration')),
            composer = info.get('Composer'),
        )
    else:
        raise BaseException(f'Inccorrect data: {content}')                
