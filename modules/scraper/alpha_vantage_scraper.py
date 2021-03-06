from datetime import date
from datetime import timedelta
from warnings import warn, simplefilter

from alpha_vantage.timeseries import TimeSeries as AlphaVantageTimeSeries
from pandas import to_datetime
from ratelimit import limits, sleep_and_retry

from modules.core import config
from modules.core.model.stock import TimeSeries, HistoricDataPoint

simplefilter('always', DeprecationWarning)
warn("This module is deprecated as Alpha Vantage is found to give inconsistent results", DeprecationWarning)


class AlphaVantageScraper:
    api_key = config.get('scraper.alpha_vantage.api_key')
    lookback_days = config.get('scraper.alpha_vantage.lookback_days')
    concurrency = config.get('scraper.alpha_vantage.concurrency')
    rate_limit = config.get('scraper.alpha_vantage.rate_limit')
    default_start_date = date.today() - timedelta(days=lookback_days)

    @sleep_and_retry
    @limits(calls=rate_limit['calls'], period=rate_limit['period'])
    def get_time_series(self, yahoo_ticker: str, start_date: date = default_start_date,
                        end_date: date = date.today()) -> TimeSeries:
        """
        Returns time series for given ticker in Yahoo finance format (e.g. HSBA.L)
        :param yahoo_ticker:
        :param start_date:
        :param end_date:
        :return:
        """
        ts = AlphaVantageTimeSeries(key=self.api_key, output_format='pandas')
        data, meta_data = ts.get_daily(symbol=yahoo_ticker, outputsize='full')
        data.index = to_datetime(data.index)
        data_truncated = data.truncate(before=start_date, after=end_date)
        return [HistoricDataPoint(
            time=dt.to_pydatetime(),
            open=row['1. open'],
            high=row['2. high'],
            low=row['3. low'],
            close=row['4. close'],
            volume=row['5. volume']
        ) for dt, row in data_truncated.iterrows()]
