from datetime import datetime
from decimal import Decimal

from binance.spot import Spot

from django_soyba.data_sources.api_interfaces.base.interface import DataSourceInterface
from django_soyba.data_sources.api_interfaces.binance.types import BinanceOhlc
from django_soyba.data_sources.api_interfaces.binance.utils import format_binance_timeframe
from django_soyba.data_sources.api_interfaces.schema import Ohlc, Timeframe, TimeframeUnit


class BinanceInterface(DataSourceInterface):
    max_ohlc_per_request = 1000

    def __init__(self):
        self.client = Spot()

    def get_ohlc_batch(
        self,
        *,
        symbol: str,
        timeframe: Timeframe,
        count: int,
        start_datetime: datetime,
    ) -> tuple[Ohlc, ...]:
        formatted_timeframe = format_binance_timeframe(timeframe)

        raw_ohlc_list: tuple[BinanceOhlc, ...] = self.client.klines(
            symbol,
            formatted_timeframe,
            limit=count,
            startTime=start_datetime.timestamp() * 1000,
        )

        return tuple(self._construct_ohlc(raw_ohlc) for raw_ohlc in raw_ohlc_list)

    @staticmethod
    def _construct_ohlc(raw_ohlc: BinanceOhlc) -> Ohlc:
        return Ohlc(
            open=Decimal(raw_ohlc[1]),
            high=Decimal(raw_ohlc[2]),
            low=Decimal(raw_ohlc[3]),
            close=Decimal(raw_ohlc[4]),
            start_time=datetime.fromtimestamp(raw_ohlc[0] / 1000),
            end_time=datetime.fromtimestamp(raw_ohlc[6] / 1000),
        )

    def get_available_instruments(self) -> tuple[str, ...]:
        def instrument_is_active(instrument):
            return instrument["status"] == "TRADING"

        def instrument_get_symbol(instrument):
            return instrument["symbol"]

        raw_instruments = self.client.exchange_info(permissions=["SPOT"])["symbols"]
        return tuple(instrument_get_symbol(i) for i in raw_instruments if instrument_is_active(i))

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
