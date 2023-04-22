from datetime import datetime
from decimal import Decimal

from binance.spot import Spot

from ..base.interface import DataSourceInterface
from ..binance.types import BinanceOHLC
from ..binance.utils import format_binance_timeframe
from ..schema import OHLC, Timeframe, TimeframeUnit


class BinanceInterface(DataSourceInterface):
    def __init__(self):
        self.client = Spot()

    def get_ohlc(self, *, symbol: str, timeframe: Timeframe, count: int, start_datetime: datetime) -> tuple[OHLC, ...]:
        formatted_timeframe = format_binance_timeframe(timeframe)

        raw_ohlc_list: tuple[BinanceOHLC] = self.client.klines(
            symbol,
            formatted_timeframe,
            limit=count,
            startTime=start_datetime.timestamp() * 1000,
        )

        return tuple(self._construct_ohlc(raw_ohlc) for raw_ohlc in raw_ohlc_list)

    @staticmethod
    def _construct_ohlc(raw_ohlc: BinanceOHLC) -> OHLC:
        return OHLC(
            open=Decimal(raw_ohlc[1]),
            high=Decimal(raw_ohlc[2]),
            low=Decimal(raw_ohlc[3]),
            close=Decimal(raw_ohlc[4]),
            start_time=datetime.fromtimestamp(raw_ohlc[0] / 1000),
            end_time=datetime.fromtimestamp(raw_ohlc[6] / 1000),
        )

    def get_available_instruments(self) -> tuple[str, ...]:
        def instrument_is_active(instrument):
            return instrument['status'] == 'TRADING'

        def instrument_get_symbol(instrument):
            return instrument['symbol']

        raw_instruments = self.client.exchange_info(permissions=["SPOT"])["symbols"]
        instruments = filter(instrument_is_active, raw_instruments)
        return tuple(map(instrument_get_symbol, instruments))

    def get_available_timeframes(self) -> tuple[Timeframe, ...]:
        return (
            Timeframe(count=1, unit=TimeframeUnit.SECOND),
            Timeframe(count=1, unit=TimeframeUnit.MINUTE),
            Timeframe(count=3, unit=TimeframeUnit.MINUTE),
            Timeframe(count=5, unit=TimeframeUnit.MINUTE),
            Timeframe(count=15, unit=TimeframeUnit.MINUTE),
            Timeframe(count=30, unit=TimeframeUnit.MINUTE),
            Timeframe(count=1, unit=TimeframeUnit.HOUR),
            Timeframe(count=2, unit=TimeframeUnit.HOUR),
            Timeframe(count=4, unit=TimeframeUnit.HOUR),
            Timeframe(count=6, unit=TimeframeUnit.HOUR),
            Timeframe(count=8, unit=TimeframeUnit.HOUR),
            Timeframe(count=12, unit=TimeframeUnit.HOUR),
            Timeframe(count=1, unit=TimeframeUnit.DAY),
            Timeframe(count=3, unit=TimeframeUnit.DAY),
            Timeframe(count=1, unit=TimeframeUnit.WEEK),
            Timeframe(count=1, unit=TimeframeUnit.MONTH),
        )
