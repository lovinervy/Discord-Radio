import pytest

from my_types.radio import StationScoreboardAddress
from radio import what_plays_on_asiadreamradio
from setup import BASIC_STATIONS

TEST_STATION = "Japan Hits"


class TestWhatPlaysOnAsiaDreamRadio:
    """Testing "what_play_on_asiadreamradio"""

    @pytest.mark.asyncio
    async def test_what_plays_on_asiadreamradio_with_correct_data(self):
        """Testing with insert correct scoreboard data"""
        scoreboard = BASIC_STATIONS[TEST_STATION].scoreboard_address
        result = await what_plays_on_asiadreamradio(scoreboard)
        assert result is not None

    @pytest.mark.asyncio
    async def test_what_plays_on_asiadreamradio_with_wrong_data(self):
        """Testing with insert wrong scoreboard data"""
        scoreboard = StationScoreboardAddress(
            url='https://example.com',
            params={
                'token': 'test',
                'format': 'json',
                '_': ''
            }
        )
        result = await what_plays_on_asiadreamradio(scoreboard)
        assert result is None

    @pytest.mark.asyncio
    async def test_what_plays_on_asiadreamradio_with_wrong_url(self):
        """Testing with insert wrong url in scoreboard data"""
        scoreboard = BASIC_STATIONS[TEST_STATION].scoreboard_address
        scoreboard.url = "https://example.com"
        result = await what_plays_on_asiadreamradio(scoreboard)
        assert result is None

    @pytest.mark.asyncio
    async def test_what_plays_on_asiadreamradio_with_wrong_params(self):
        """Testing with insert wrong params in scoreboard data"""
        scoreboard = BASIC_STATIONS[TEST_STATION].scoreboard_address
        scoreboard.params["token"] = "testtesttest"
        result = await what_plays_on_asiadreamradio(scoreboard)
        assert result is None

    @pytest.mark.asyncio
    async def test_what_plays_on_asiadreamradio_without_params(self):
        """Testing without params in scoreboard data"""
        scoreboard = BASIC_STATIONS[TEST_STATION].scoreboard_address
        scoreboard.params = None
        result = await what_plays_on_asiadreamradio(scoreboard)
        assert result is None
