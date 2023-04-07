from collections.abc import Iterable
from datetime import datetime

from data_sources.api_interfaces.schema import OHLC, Timeframe


class DataSourceInterface:
    def get_ohlc(self, *, symbol: str, timeframe: Timeframe, count: int, start_datetime: datetime) -> Iterable[OHLC]:
        raise NotImplementedError