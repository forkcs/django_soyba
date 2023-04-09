from collections.abc import Iterable
from datetime import datetime
from decimal import Decimal

from kraken.spot import Market

from ..base.interface import DataSourceInterface
from ..schema import OHLC, Timeframe, TimeframeUnit
from .types import KrakenOHLC


class KrakenInterface(DataSourceInterface):
    def __init__(self):
        self.market = Market()

    @staticmethod
    def _construct_ohlc(raw_ohlc: KrakenOHLC) -> OHLC:
        """Not sure if it's correct"""
        return OHLC(
            open=Decimal(raw_ohlc[1]),
            high=Decimal(raw_ohlc[2]),
            low=Decimal(raw_ohlc[3]),
            close=Decimal(raw_ohlc[4]),
            start_time=datetime.fromtimestamp(raw_ohlc[0]),
        )

    @staticmethod
    def _minutes_from_timeframe(timeframe: Timeframe) -> float:
        MINUTES_BY_UNIT = {
            TimeframeUnit.SECOND: 1 / 60,
            TimeframeUnit.MINUTE: 1,
            TimeframeUnit.HOUR: 60,
            TimeframeUnit.DAY: 24 * 60,
            TimeframeUnit.MONTH: 24 * 60 * 30,
            TimeframeUnit.YEAR: 24 * 60 * 365,
        }

        try:
            return float(timeframe.count * MINUTES_BY_UNIT[timeframe.unit])
        except KeyError:
            raise ValueError("Unknown TimeframeUnit value")

    def get_ohlc(self, *, symbol: str, timeframe: Timeframe, count: int, start_datetime: datetime) -> tuple[OHLC]:
        raw_ohlc_dict: dict[str, list[KrakenOHLC]] = self.market.get_ohlc(
            symbol, int(self._minutes_from_timeframe(timeframe)), int(start_datetime.timestamp())
        )
        raw_ohlc_list: list[KrakenOHLC] = raw_ohlc_dict[tuple(raw_ohlc_dict.keys())[0]][:count]
        return tuple(map(self._construct_ohlc, raw_ohlc_list))

    def get_available_instruments(self) -> Iterable[str]:
        return self.market.get_assets().keys()

    def get_available_timeframes(self) -> Iterable[Timeframe]:
        return (
            Timeframe(count=1, unit=TimeframeUnit.MINUTE),
            Timeframe(count=5, unit=TimeframeUnit.MINUTE),
            Timeframe(count=15, unit=TimeframeUnit.MINUTE),
            Timeframe(count=60, unit=TimeframeUnit.MINUTE),
            Timeframe(count=240, unit=TimeframeUnit.MINUTE),
            Timeframe(count=1440, unit=TimeframeUnit.MINUTE),
            Timeframe(count=10080, unit=TimeframeUnit.MINUTE),
            Timeframe(count=21600, unit=TimeframeUnit.MINUTE),
        )
