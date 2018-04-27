import pytest

from modules.scraper.lse_scraper import Index, LSEScraper


@pytest.fixture
def scraper():
    return LSEScraper()


def test_get_ftse_100_constituents(scraper):
    constituents = scraper.get_constituents(Index.FTSE100)
    tickers = [ticker for ticker, _ in constituents]
    assert 'BARC.L' in tickers
    assert 'GSK.L' in tickers


def test_get_ftse_250_constituents(scraper):
    constituents = scraper.get_constituents(Index.FTSE250)
    tickers = [ticker for ticker, _ in constituents]
    assert 'BGFD.L' in tickers
    assert 'WIZZ.L' in tickers
