from datetime import datetime

import data_sources.api_interfaces.schema as schema
from data_sources import get_interface_by_data_source_name
from market_data.models.ohlc import OHLC, Instrument


class MarketDataFetcher:
    """Class for fetching market data and storing it in the database."""

    def fetch_ohlc(
        self, data_source_name: str, symbol: str, count: int, timeframe: schema.Timeframe, start_datetime: datetime
    ) -> None:
        interface = get_interface_by_data_source_name(data_source_name)()
        ohlc_seq = interface.get_ohlc(symbol=symbol, count=count, timeframe=timeframe, start_datetime=start_datetime)
        for ohlc in ohlc_seq:
            OHLC(ohlc).save()

    def fetch_available_instruments(self, data_source_name: str) -> None:
        interface = get_interface_by_data_source_name(data_source_name)()
        instruments_seq = interface.get_available_instruments()
        for instrument in instruments_seq:
            Instrument(instrument).save()
