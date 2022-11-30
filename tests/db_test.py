import pytest

from db.database import Connect, RadioActivity
from db.engine import SQLite
from my_types.radio import Station, StationAddress, StationScoreboardAddress

TEST_DB = 'test_db.database'
STATION_NAME = 'test'
STATION_NAME2 = 'test2'
STATION_ADDRESS = StationAddress('http://radio.com/', {'test': 'radio'})
SCOREBOARD_ADDRESS = StationScoreboardAddress(
    'http://scoreboard.com/', {'test': 'scoreboard'})
STATION = Station('test', STATION_ADDRESS, SCOREBOARD_ADDRESS)
DATA_SCOREBOARD1 = "MusicInfo Test 1"
DATA_SCOREBOARD2 = "MusicInfo Test 2"
CHANNEL_ID = 123
GUILD_ID = 321
RADIO_ACTIVITY = RadioActivity(STATION_NAME, GUILD_ID, CHANNEL_ID)


@pytest.fixture(autouse=True, scope="module", name="database")
def setup_db(tmpdir_factory):
    """Init connector to database"""
    temp_dir = tmpdir_factory.mktemp('temp')
    engine = SQLite(db_path=f"{str(temp_dir)}/{TEST_DB}")
    connector = Connect(engine)
    yield connector


def test_set_radio(database):
    """Test insert data into radio table"""
    radio = [
        STATION_NAME, STATION_ADDRESS.url, STATION_ADDRESS.params,
        SCOREBOARD_ADDRESS.url, SCOREBOARD_ADDRESS.params
    ]
    database.set_radio(*radio)


def test_set_radio_without_scoreboard(database):
    """Test insert radio data without scoreboard data into database"""
    radio = [STATION_NAME2,  STATION_ADDRESS.url, STATION_ADDRESS.params]
    database.set_radio(*radio)


def test_get_radio_list(database):
    """Test get all data from radio table"""
    assert database.get_radio_list() == [STATION_NAME, STATION_NAME2]


def test_get_radio_station_address(database):
    """Test get data from station address table"""
    assert database.get_radio_station_address(STATION_NAME) == STATION_ADDRESS


def test_get_radio_scoreboard_address(database):
    """Test get data from scoreboard address table"""
    assert database.get_radio_scoreboard_address(
        STATION_NAME) == SCOREBOARD_ADDRESS


def test_get_radio(database):
    """Test get data from radio table"""
    assert database.get_radio(STATION_NAME) == STATION


def test_set_radio_activity(database):
    """Test insert data to radio activity table"""
    activity = [GUILD_ID, CHANNEL_ID, STATION_NAME]
    database.set_radio_activity(*activity)


def test_get_radio_activity(database):
    """Test get data from radio activity"""
    assert database.get_radio_activity() == [RADIO_ACTIVITY,]


def test_delete_radio_activity(database):
    """Test delete data from radio activity table"""
    database.delete_radio_activity(GUILD_ID)
    assert database.get_radio_activity() is None


def test_set_last_scoreboard(database):
    """Test insert to last scoreboard table"""
    database.set_last_scoreboard(STATION_NAME, DATA_SCOREBOARD1)


def test_get_last_scoreboard(database):
    """Test get data from last scoreboard table"""
    assert database.get_last_scoreboard(STATION_NAME) == DATA_SCOREBOARD1


def test_update_last_scoreboard(database):
    """Test update data from last scoreboard table"""
    database.update_last_scoreboard(STATION_NAME, DATA_SCOREBOARD2)
    assert database.get_last_scoreboard(STATION_NAME) == DATA_SCOREBOARD2


def test_delete_last_scoreboard(database):
    """Test delete from last scoreboard table"""
    database.delete_last_scoreboard(STATION_NAME)
    assert database.get_last_scoreboard(STATION_NAME) is None


def test_set_current_scoreboard(database):
    """Test insert data to current scoreboard table"""
    database.set_current_scoreboard(STATION_NAME, DATA_SCOREBOARD1)


def test_get_current_scoreboard(database):
    """Test get data from current scoreboard table"""
    scoreboard = database.get_current_scoreboard(STATION_NAME)
    assert scoreboard == DATA_SCOREBOARD1


def test_update_current_scoreboard(database):
    """Test update data in current scoreboard table"""
    database.update_current_scoreboard(STATION_NAME, DATA_SCOREBOARD2)
    assert database.get_current_scoreboard(STATION_NAME) == DATA_SCOREBOARD2


def test_delete_current_scoreboard(database):
    """Test delete from current scorebaord table"""
    database.delete_current_scoreboard(STATION_NAME)
    assert database.get_current_scoreboard(STATION_NAME) is None


def test_get_from_silence_group(database):
    """Test get from silence group table"""
    assert database.get_from_silence_group(GUILD_ID) is None


def test_add_in_silence_group(database):
    """Test insert to silence group table"""
    database.add_in_silence_group(GUILD_ID)
    assert database.get_from_silence_group(GUILD_ID) == (1, GUILD_ID)


def test_delete_from_silence_group(database):
    """Test delete from silence group table"""
    database.delete_from_silence_group(GUILD_ID)
    assert database.get_from_silence_group(GUILD_ID) is None
