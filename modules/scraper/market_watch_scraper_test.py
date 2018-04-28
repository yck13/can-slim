import pytest

from modules.scraper.market_watch_scraper import MarketWatchScraper
from datetime import datetime


@pytest.fixture
def scraper():
    return MarketWatchScraper()


def test_get_time_series(scraper):
    time_series = scraper.get_time_series(ticker='HSBA', step='P1D', timeframe='P5D')
    assert 3 <= len(time_series) <= 5
    for point in time_series:
        assert type(point.time) == datetime
        assert point.open > 0
        assert point.high > 0
        assert point.low > 0
        assert point.close > 0
        assert point.volume > 0
        assert point.high >= point.open >= point.low
        assert point.high >= point.close >= point.low