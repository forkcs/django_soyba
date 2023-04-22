from collections.abc import Collection, Iterable, Sequence
from datetime import datetime
from typing import ClassVar, final

from data_sources.api_interfaces.schema import OHLC, Timeframe


class DataSourceInterface:
    max_ohlc_per_request: ClassVar[int]

    @final
    def get_ohlc(self, *, symbol: str, timeframe: Timeframe, count: int, start_datetime: datetime) -> Sequence[OHLC]:
        ohlc_batches = self.split_ohlc_request(
            symbol=symbol, timeframe=timeframe, count=count, start_datetime=start_datetime
        )
        return tuple(ohlc for ohlc_batch in ohlc_batches for ohlc in ohlc_batch)

    def get_ohlc_batch(
        self, *, symbol: str, timeframe: Timeframe, count: int, start_datetime: datetime
    ) -> Sequence[OHLC]:
        raise NotImplementedError

    def split_ohlc_request(
        self, *, symbol: str, timeframe: Timeframe, count: int, start_datetime: datetime
    ) -> Iterable[Sequence[OHLC]]:
        remaining_count = count
        start_datetime = start_datetime
        while remaining_count > 0:
            current_count = min(remaining_count, self.max_ohlc_per_request)
            yield self.get_ohlc_batch(
                symbol=symbol, timeframe=timeframe, count=current_count, start_datetime=start_datetime
            )
            remaining_count -= current_count
            start_datetime += timeframe.interval * current_count

    def get_available_instruments(self) -> Collection[str]:
        raise NotImplementedError

    def get_available_timeframes(self) -> Collection[Timeframe]:
        raise NotImplementedError
