import pytest
import os

from db.database import Connect
from radio import Station, StationAddress, StationScoreboardAddress


TEST_DB_PATH = 'tests/test_db.db'
STATION_NAME = 'test'
STATION_ADDRESS = StationAddress('http://radio.com/', {'test': 'radio'})
SCOREBOARD_ADDRESS = StationScoreboardAddress('http://scoreboard.com/', {'test': 'scoreboard'})
STATION = Station('test', STATION_ADDRESS, SCOREBOARD_ADDRESS)

CHANNEL_ID = 123
GUILD_ID = 321


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    try:
        test_base = Connect(db_path=TEST_DB_PATH)
        
        radio = [
            STATION_NAME, STATION_ADDRESS.url, STATION_ADDRESS.params,
            SCOREBOARD_ADDRESS.url, SCOREBOARD_ADDRESS.params
        ]
        test_base.set_radio(*radio)

        activity = [GUILD_ID, CHANNEL_ID, STATION_NAME]
        test_base.set_radio_activity(*activity)

        yield test_base
    finally:
        os.remove(TEST_DB_PATH)    


def test_get_radio_list(setup_db):
   assert setup_db.get_radio_list() == [STATION_NAME]


def test_get_radio_station_address(setup_db):
    assert setup_db.get_radio_station_address(STATION_NAME) == STATION_ADDRESS


def test_get_radio_scoreboard_address(setup_db):
    assert setup_db.get_radio_scoreboard_address(STATION_NAME) == SCOREBOARD_ADDRESS


def test_get_radio(setup_db):
    assert setup_db.get_radio(STATION_NAME) == STATION


def test_get_radio_activity(setup_db):
    assert setup_db.get_radio_activity() == [(STATION_NAME, GUILD_ID, CHANNEL_ID),]


def test_unset_radio_activity(setup_db):
    setup_db.unset_radio_activity(GUILD_ID)
    assert setup_db.get_radio_activity() == []