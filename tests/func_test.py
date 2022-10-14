import pytest

from db.database import Connect
from radio import what_plays_on_asiadreamradio
from tests.db_test import STATION_NAME2

RADIO = "Japan Hits"


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    db = Connect()
    yield db

@pytest.mark.asyncio
async def test_what_plays_on_asiadreamradio_true_radio(setup_db):
    scoreboard = setup_db.get_radio_scoreboard_address(RADIO)
    result = await what_plays_on_asiadreamradio(scoreboard)
    assert result != None


@pytest.mark.asyncio
async def test_what_plays_on_asiadreamradio_fake_radio(setup_db):
    scoreboard = setup_db.get_radio_scoreboard_address(STATION_NAME2)
    result = await what_plays_on_asiadreamradio(scoreboard)
    assert result == None
