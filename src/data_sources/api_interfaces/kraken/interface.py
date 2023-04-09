from collections.abc import Iterable
from datetime import datetime
from decimal import Decimal

from kraken.spot import Market

from ..base.interface import DataSourceInterface
from .types import KrakenOHLC
from ..schema import OHLC, Timeframe, TimeframeUnit


class KrakenInterface(DataSourceInterface):
    def __init__(self):
        self.market = Market()

    def get_ohlc(self, *, symbol: str, timeframe: Timeframe, count: int, start_datetime: datetime) -> Iterable[OHLC]:
        """ TODO: What about unused count?.. """
        return self.market.get_ohlc(symbol, int(timeframe.minutes), int(start_datetime.timestamp()))
