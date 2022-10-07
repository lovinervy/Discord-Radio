from dataclasses import dataclass
import time
import requests


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

    def __str__(self) -> str:
        return self.__formatted_text

    def __repr__(self) -> str:
        return self.__formatted_text


STATIONS = {
    "J-Pop Powerplay Kawaii": Station(
        name='J-Pop Powerplay Kawaii',
        station_address=StationAddress(
            url='https://kathy.torontocast.com:3060/;',
            params={
                'type': 'http'
            }
        ),
        scoreboard_address=StationScoreboardAddress(
            url='https://listen.samcloud.com/webapi/station/77836/history/npe',
            params={
                'token': '17ea9158ac026e12bff74db9bddbf8a6de2c23cd',
                'format': 'json',
                '_': ''
            }
        )
    ),
    'Japan Hits': Station(
        name='Japan Hits',
        station_address=StationAddress(
            url='https://igor.torontocast.com:1025/;',
            params={
                'type': 'http'
            }
        ),
        scoreboard_address=StationScoreboardAddress(
            url='https://listen.samcloud.com/webapi/station/78063/history/npe',
            params={
                'token': 'cf8d100d2f5e841ecdb8428e14bab72b1b281bfe',
                'format': 'json',
                '_': ''
            }
        )
    ),
    'J-Pop Powerplay': Station(
        name='J-Pop Powerplay',
        station_address=StationAddress(
            url='https://kathy.torontocast.com:3560/;',
            params={
                'type': 'http'
            }
        ),
        scoreboard_address=StationScoreboardAddress(
            url='https://listen.samcloud.com/webapi/station/101976/history/npe',
            params={
                'token': '6075532892f2f66b3a45468a26d8b61403c0152a',
                'format': 'json',
                '_': ''
            }
        )
    ),
    'J-Pop Sakura 懐かしい': Station(
        name='J-Pop Sakura 懐かしい',
        station_address=StationAddress(
            url='https://igor.torontocast.com:1710/;',
            params={
                'type': 'http'
            }
        ),
        scoreboard_address=StationScoreboardAddress(
            url='https://listen.samcloud.com/webapi/station/77726/history/npe',
            params={
                'token': 'cb8691400659ddb378bb39eb53bd8a7ae653161b',
                'format': 'json',
                '_': ''
            }
        )
    ),
    'J-Rock Powerplay': Station(
        name='J-Rock Powerplay',
        station_address=StationAddress(
            url='https://kathy.torontocast.com:3340/;',
            params={
                'type': 'http'
            }
        ),
        scoreboard_address=StationScoreboardAddress(
            url='https://listen.samcloud.com/webapi/station/78062/history/npe',
            params={
                'token': 'e01dfb25370ccec1df2bd96c15d47ff89b6bb62f',
                'format': 'json',
                '_': ''
            }
        )
    ),
    'J-Club Powerplay HipHop': Station(
        name='J-Club Powerplay HipHop',
        station_address=StationAddress(
            url='https://kathy.torontocast.com:3350/;',
            params={
                'type': 'http'
            }
        ),
        scoreboard_address=StationScoreboardAddress(
            url='https://listen.samcloud.com/webapi/station/77996/history/npe',
            params={
                'token': '889c64fbb7226ba0e03334e7490badae370d6402',
                'format': 'json',
                '_': ''
            }
        )
    )
}


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
    scoreboard.params['_'] = time.time() // 1
    return scoreboard


def __request_get(url: str, params: dict) -> requests.Response:
    response = requests.get(url=url, params=params)
    if response.status_code != 200:
        raise requests.exceptions.ConnectionError(f'Error:\nurl: {url}\nparams: {params}\nstatus code: {response.status_code}\nResponse: {response.text}')
    return response


def what_plays_on_asiadreamradio(station_name: str) -> MusicInfo:
    station = STATIONS.get(station_name)
    if not station:
        raise BaseException(f'Station "{station_name}" not found')

    scoreboard = station.scoreboard_address

    scoreboard = __update_time_in_scoreboard(scoreboard)
    station.scoreboard_address = scoreboard

    response = __request_get(url=scoreboard.url, params=scoreboard.params)
    content: dict = response.json()

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


if __name__ == '__main__':
    radio = 'J-Club Powerplay HipHop'
    print('&'.join(['='.join(x) for x in STATIONS[radio].station_address.params.items()]))