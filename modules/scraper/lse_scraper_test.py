import pytest

from modules.core.model.index import Index, IndexConstituent
from modules.scraper.lse_scraper import LSEScraper


@pytest.fixture
def scraper():
    return LSEScraper()


def test_get_ftse_100_constituents(scraper):
    constituents = scraper.get_constituents(Index.FTSE100)
    barclays = IndexConstituent(ticker='BARC', name='BARCLAYS', currency='GBX')
    gsk = IndexConstituent(ticker='GSK', name='GLAXOSMITHKLINE', currency='GBX')
    assert barclays in constituents
    assert gsk in constituents


def test_get_ftse_250_constituents(scraper):
    constituents = scraper.get_constituents(Index.FTSE250)
    baillie = IndexConstituent(ticker='BGFD', name='BAILLIE G.JAP.', currency='GBX')
    wizz_air = IndexConstituent(ticker='WIZZ', name='WIZZ AIR', currency='GBX')
    assert baillie in constituents
    assert wizz_air in constituents
