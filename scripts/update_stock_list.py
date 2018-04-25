from modules.scraper.lse_scraper import LSEScraper
from modules.core.model.index import Index, IndexConstituent
from modules.core.db.access.conn import start_connection
from modules.core.db.access.stock_util import list_stocks


def get_constituents() -> [IndexConstituent]:
    scraper = LSEScraper()
    ftse100_constituents = scraper.get_constituents(Index.FTSE100)
    ftse250_constituents = scraper.get_constituents(Index.FTSE250)
    return ftse100_constituents + ftse250_constituents


if __name__ == '__main__':
    start_connection()
    old_stocks = list_stocks()
    new_stocks = LSEScraper().get_constituents(Index.FTSE250)
    print(new_stocks)
