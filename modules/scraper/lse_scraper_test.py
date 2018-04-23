from modules.scraper.lse_scraper import LSEScraper
from modules.core.model.index import Index
from modules.core.model.index import Constituent

def test_get_ftse_100_constituents():
    scraper = LSEScraper()
    constituents = scraper.get_constituents(Index.FTSE100)
    barclays = Constituent(ticker='BARC', name='BARCLAYS', currency='GBX')
    gsk = Constituent(ticker='GSK', name='GLAXOSMITHKLINE', currency='GBX')
    assert barclays in constituents
    assert gsk in constituents

def test_get_ftse_250_constituents():
    scraper = LSEScraper()
    constituents = scraper.get_constituents(Index.FTSE250)
    baillie = Constituent(ticker='BGFD', name='BAILLIE G.JAP.', currency='GBX')
    wizz_air = Constituent(ticker='WIZZ', name='WIZZ AIR', currency='GBX')
    assert baillie in constituents
    assert wizz_air in constituents