from db.database import Connect
from radio import Station, StationAddress, StationScoreboardAddress 

BASIC_STATIONS = {
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

def add_radio(db):
    radio_list = db.get_radio_list()
    for radio, data in BASIC_STATIONS.items():
        if radio not in radio_list:
            db.set_radio(
                radio,
                data.station_address.url,
                data.station_address.params,
                data.scoreboard_address.url,
                data.scoreboard_address.params
            )
    