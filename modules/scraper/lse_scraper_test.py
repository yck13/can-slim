import pytest

from modules.core.model.index import Index
from modules.scraper.lse_scraper import LSEScraper


@pytest.fixture
def scraper():
    return LSEScraper()


def test_get_ftse_100_constituents(scraper):
    constituents = scraper.get_constituents(Index.FTSE100)
    assert 'BARC' in constituents
    assert 'GSK' in constituents


def test_get_ftse_250_constituents(scraper):
    constituents = scraper.get_constituents(Index.FTSE250)
    assert 'BGFD' in constituents
    assert 'WIZZ' in constituents
