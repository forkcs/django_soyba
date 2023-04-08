from datetime import datetime
from decimal import Decimal
from typing import Iterable

from binance.spot import Spot

from ..base.interface import DataSourceInterface
from ..binance.types import BinanceOHLC
from ..binance.utils import format_binance_timeframe
from ..schema import OHLC, Timeframe


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

    def get_available_instruments(self) -> Iterable[str]:
        instruments = self.client.exchange_info(permissions=["SPOT"])
        return instruments

    def get_available_timeframes(self) -> Iterable[Timeframe]:
        TIMEFRAMES = ("1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M")
        return map(Timeframe.construct, TIMEFRAMES)
