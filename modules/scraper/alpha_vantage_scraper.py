from datetime import date
from datetime import timedelta

from alpha_vantage.timeseries import TimeSeries as AlphaVantageTimeSeries
from pandas import to_datetime

from modules.core import config
from modules.core.model.stock import TimeSeries, HistoricDataPoint


class AlphaVantageScraper:
    def __init__(self):
        self.api_key = config.get('scraper.alpha_vantage.api_key')
        self.lookback_days = config.get('scraper.alpha_vantage.lookback_days')
        self.default_start_date = date.today() - timedelta(days=self.lookback_days)
        self.default_end_date = date.today()

    def get_time_series(self, ticker: str, start_date: date = None, end_date: date = None) -> TimeSeries:
        """
        scrapes and returns the list of underlying commpany tickers of index (e.g. UKX)
        :param index:
        :return:
        """
        if not start_date:
            start_date = self.default_start_date
        if not end_date:
            end_date = self.default_end_date

        ts = AlphaVantageTimeSeries(key=self.api_key, output_format='pandas')
        data, meta_data = ts.get_daily(symbol=ticker, outputsize='full')
        data.index = to_datetime(data.index)
        data_truncated = data.truncate(before=start_date, after=end_date)
        return [HistoricDataPoint(date=dt, price=row['4. close'], volume=row['5. volume']) for dt, row in
                data_truncated.iterrows()]
