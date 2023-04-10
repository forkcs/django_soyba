from datetime import datetime
from decimal import Decimal

from pybit.unified_trading import HTTP

from data_sources.api_interfaces.bybit.types import BybitOHLC

from ..base.interface import DataSourceInterface
from ..schema import OHLC, Timeframe, TimeframeUnit


class BybitInterface(DataSourceInterface):
    def __init__(self):
        self.session = HTTP()

    @staticmethod
    def _construct_ohlc(raw_ohlc: BybitOHLC) -> OHLC:
        return OHLC(
            open=Decimal(raw_ohlc[1]),
            high=Decimal(raw_ohlc[2]),
            low=Decimal(raw_ohlc[3]),
            close=Decimal(raw_ohlc[4]),
            start_time=datetime.fromtimestamp(float(raw_ohlc[0]) / 1000),
        )

    @staticmethod
    def _minutes_from_timeframe(timeframe: Timeframe) -> float:
        MINUTE_BY_UNIT: dict[TimeframeUnit, float] = {
            TimeframeUnit.SECOND: 1 / 60.0,
            TimeframeUnit.MINUTE: 1.0,
            TimeframeUnit.HOUR: 60.0,
            TimeframeUnit.DAY: 24 * 60.0,
            TimeframeUnit.WEEK: 7 * 24 * 60.0,
            TimeframeUnit.MONTH: 30 * 24 * 60.0,
            TimeframeUnit.YEAR: 356 * 24 * 60.0,
        }
        return float(timeframe.count * MINUTE_BY_UNIT[timeframe.unit])

    def _get_instruments_info(self, *args, **kwargs) -> dict:
        """This method is just a workaround of invalid return type hint of `pybit.HTTP.get_instruments_info`."""
        return self.session.get_instruments_info(*args, **kwargs)  # type: ignore

    def get_ohlc(self, *, symbol: str, timeframe: Timeframe, count: int, start_datetime: datetime) -> tuple[OHLC, ...]:
        minutes: float = self._minutes_from_timeframe(timeframe)
        raw_ohlc_list: dict = self.session.get_kline(
            category='spot', symbol=symbol, interval=f'{minutes}', limit=count, start=start_datetime.timestamp()
        )["result"]["list"]
        return tuple(map(self._construct_ohlc, raw_ohlc_list))

    def get_available_instruments(self) -> tuple[str, ...]:
        def instrument_is_active(instrument: dict) -> bool:
            return instrument["status"] == "Trading"

        def instrument_get_symbol(instrument: dict) -> str:
            return instrument["symbol"]

        raw_instruments = self._get_instruments_info(category='spot')["result"]["list"]
        return tuple(map(instrument_get_symbol, filter(instrument_is_active, raw_instruments)))

    def get_available_timeframes(self) -> tuple[Timeframe, ...]:
        """Not sure about days, weeks, and months"""
        return (
            Timeframe(count=1, unit=TimeframeUnit.MINUTE),
            Timeframe(count=3, unit=TimeframeUnit.MINUTE),
            Timeframe(count=5, unit=TimeframeUnit.MINUTE),
            Timeframe(count=15, unit=TimeframeUnit.MINUTE),
            Timeframe(count=30, unit=TimeframeUnit.MINUTE),
            Timeframe(count=60, unit=TimeframeUnit.MINUTE),
            Timeframe(count=120, unit=TimeframeUnit.MINUTE),
            Timeframe(count=240, unit=TimeframeUnit.MINUTE),
            Timeframe(count=360, unit=TimeframeUnit.MINUTE),
            Timeframe(count=720, unit=TimeframeUnit.MINUTE),
            Timeframe(count=1, unit=TimeframeUnit.DAY),
            Timeframe(count=1, unit=TimeframeUnit.WEEK),
            Timeframe(count=1, unit=TimeframeUnit.MONTH),
        )
