import pytest

from modules.scraper.lse_scraper import Index, LSEScraper


@pytest.fixture
def scraper():
    return LSEScraper()


def test_get_ftse_100_constituents(scraper):
    constituents = scraper.get_constituents(Index.FTSE100)
    assert 'BARC.L' in constituents
    assert 'GSK.L' in constituents


def test_get_ftse_250_constituents(scraper):
    constituents = scraper.get_constituents(Index.FTSE250)
    assert 'BGFD.L' in constituents
    assert 'WIZZ.L' in constituents
