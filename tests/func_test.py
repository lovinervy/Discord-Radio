import os
import pytest

from db.engine import SQLite
from db.database import Connect
from setup import add_radio
from radio import what_plays_on_asiadreamradio
from tests.db_test import STATION_NAME2, TEST_DB_PATH

RADIO = "Japan Hits"

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    try:
        engine = SQLite(TEST_DB_PATH)
        db = Connect(engine)
        add_radio(db)
        
        yield db
    finally:
        os.remove(TEST_DB_PATH)


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