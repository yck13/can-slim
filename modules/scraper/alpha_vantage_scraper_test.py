from datetime import datetime

import pytest

from modules.scraper.alpha_vantage_scraper import AlphaVantageScraper


@pytest.fixture
def scraper():
    return AlphaVantageScraper()


def test_get_time_series(scraper):
    time_series = scraper.get_time_series(ticker='MSFT')
    assert len(time_series)

    historic_data_point = time_series[0]
    assert type(historic_data_point.time) == datetime
    assert historic_data_point.price > 0
    assert historic_data_point.volume > 0
