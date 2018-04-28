import pytest

from modules.scraper.lse_scraper import Index, LSEScraper


@pytest.fixture
def scraper():
    return LSEScraper()


def test_get_ftse_100_constituents(scraper):
    constituents = scraper.get_constituents(Index.FTSE100)
    tickers = [ticker for ticker, _ in constituents]
    assert 'BT.A' in tickers
    assert 'GSK' in tickers


def test_get_ftse_250_constituents(scraper):
    constituents = scraper.get_constituents(Index.FTSE250)
    tickers = [ticker for ticker, _ in constituents]
    assert 'BGFD' in tickers
    assert 'WIZZ' in tickers
