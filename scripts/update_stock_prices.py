from modules.core.db.access.stock import list_stock_tickers
from modules.core.log import get_logger
from modules.scraper.alpha_vantage_scraper import AlphaVantageScraper

_log = get_logger(__file__)

if __name__ == '__main__':
    stock_tickers = list_stock_tickers()
    _log.debug('Will update tickers: {}'.format(stock_tickers))

    t = stock_tickers[0]
    df = AlphaVantageScraper().get_time_series(ticker=t)
    print(df)
