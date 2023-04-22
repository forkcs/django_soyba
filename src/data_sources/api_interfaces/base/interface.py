from collections.abc import Collection, Sequence
from datetime import datetime
from typing import ClassVar

from data_sources.api_interfaces.schema import OHLC, Timeframe


class DataSourceInterface:
    max_ohlc_per_request: ClassVar[int]

    def get_ohlc(self, *, symbol: str, timeframe: Timeframe, count: int, start_datetime: datetime) -> Sequence[OHLC]:
        raise NotImplementedError

    def get_available_instruments(self) -> Collection[str]:
        raise NotImplementedError

    def get_available_timeframes(self) -> Collection[Timeframe]:
        raise NotImplementedError
