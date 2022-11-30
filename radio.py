import json
import time
import datetime
import re
import aiohttp

from my_types.radio import MusicInfo, StationScoreboardAddress


def wtf_time_to_std_time(wtf_time: str = None) -> str:
    '''
    Get wtf_time type(str) as "PT0M00.000S"
    return type(str) as mm:ss.ms as "00:00.000"
    '''
    regex_result = re.match(r"^.{2}(\d+).(\d+).(\d+)", wtf_time)
    if regex_result is None:
        return "00:00.000"
    minute, secs, millisecs = map(int, regex_result.groups())
    duration = datetime.time(0, minute, secs, millisecs*1000)
    return duration.strftime("%M:%S.%f")[:-3]


def __update_time_in_scoreboard(scoreboard: StationScoreboardAddress) -> StationScoreboardAddress:
    scoreboard.params['_'] = str(int(time.time() // 1))
    return scoreboard


async def __request_get(url: str, params: dict):
    with open('headers.json', 'r', encoding="utf-8") as json_file:
        headers = json.load(json_file)
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params, headers=headers) as response:
            if response.status == 200:
                data = await response.text()
            else:
                return None
    return data


async def what_plays_on_asiadreamradio(scoreboard: StationScoreboardAddress) -> MusicInfo | None:
    """Getting info about current song play in asiadreamradio"""
    if scoreboard is None or scoreboard.params is None:
        return None
    __update_time_in_scoreboard(scoreboard)
    response = await __request_get(scoreboard.url, scoreboard.params)
    if response is None:
        return None
    try:
        content: dict = json.loads(response)
        info = content.get('m_Item2')
        assert info is not None
        return MusicInfo(
            artist=info.get('Artist'),
            title=info.get('Title'),
            year=info.get('Year'),
            duration=wtf_time_to_std_time(info.get('Duration')),
            composer=info.get('Composer'),
        )
    except json.decoder.JSONDecodeError:
        return None
