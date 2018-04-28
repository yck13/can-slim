from datetime import datetime

import pytest

from modules.scraper.alpha_vantage_scraper import AlphaVantageScraper


@pytest.fixture
def scraper():
    return AlphaVantageScraper()


@pytest.mark.skip(reason="Alpha Vantage API is unreliable, sometimes give missing data")
def test_get_time_series(scraper):
    time_series = scraper.get_time_series(yahoo_ticker='TSCO.L')
    assert len(time_series) > 0

    for point in time_series:
        assert type(point.time) == datetime
        assert point.open > 0
        assert point.high > 0
        assert point.low > 0
        assert point.close > 0
        assert point.high >= point.open >= point.low
        assert point.high >= point.close >= point.low
        assert point.volume > 0
