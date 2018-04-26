from modules.scraper.lse_scraper import LSEScraper
from modules.core.model.index import Index
from modules.core.db.access.stock import list_stock_tickers
from typing import List


def scrape_stock_tickers() -> List[str]:
    scraper = LSEScraper()
    ftse100_tickers = scraper.get_constituents(Index.FTSE100)
    ftse250_tickers = scraper.get_constituents(Index.FTSE250)
    return ftse100_tickers + ftse250_tickers


if __name__ == '__main__':
    old_stock_tickers = list_stock_tickers()
    new_stock_tickers = scrape_stock_tickers()


    print(old_stock_tickers)
    print(new_stock_tickers)
