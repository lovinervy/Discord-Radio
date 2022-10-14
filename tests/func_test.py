import pytest

from db.database import Connect
from radio import what_plays_on_asiadreamradio


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    db = Connect()
    yield db

@pytest.mark.asyncio
async def test_what_plays_on_asiadreamradio(setup_db):
    scoreboard = setup_db.get_radio_scoreboard_address('Japan Hits')
    result = await what_plays_on_asiadreamradio(scoreboard)
    assert result != None