from collections.abc import Sequence
from datetime import date, datetime

import data_sources.api_interfaces.schema as schema
import market_data.models as market_data_models
from data_sources.api_interfaces.base.interface import DataSourceInterface
from data_sources.helpers import get_interface_class_by_data_source_name
from market_data.services.ohlc import create_or_update_ohlc_seq


class MarketDataFetcher:
    def fetch_ohlc_with_min_timeframe(
        self, instrument: market_data_models.Instrument, start_date: date, end_date: date
    ) -> Sequence[schema.OHLC]:
        interface = self._get_interface_for_instrument(instrument)

        timeframe = self._get_minimal_timeframe(interface)
        count = self._get_count_for_timeframe(timeframe, start_date, end_date)
        start_datetime = datetime(start_date.year, start_date.month, start_date.day)

        return interface.get_ohlc(
            symbol=instrument.symbol, timeframe=timeframe, count=count, start_datetime=start_datetime
        )

    def _get_interface_for_instrument(self, instrument: market_data_models.Instrument) -> DataSourceInterface:
        interface_class = get_interface_class_by_data_source_name(instrument.market_data_source)
        return interface_class()

    def _get_minimal_timeframe(self, interface: DataSourceInterface) -> schema.Timeframe:
        return min(interface.get_available_timeframes())

    def _get_count_for_timeframe(self, timeframe: schema.Timeframe, start_date: date, end_date: date) -> int:
        timedelta = end_date - start_date
        return timedelta // timeframe.interval


class MarketDataSaver:
    def save_ohlc(self, *, instrument_id: int, ohlc_seq: Sequence[schema.OHLC]) -> None:
        ohlc_objects = [
            self._construct_ohlc_object(instrument_id=instrument_id, ohlc=ohlc_item) for ohlc_item in ohlc_seq
        ]
        create_or_update_ohlc_seq(ohlc_objects)

    def _construct_ohlc_object(self, *, instrument_id: int, ohlc: schema.OHLC) -> market_data_models.OHLC:
        return market_data_models.OHLC(
            instrument_id=instrument_id,
            start_time=ohlc.start_time,
            end_time=ohlc.end_time,
            open=ohlc.open,
            close=ohlc.close,
            low=ohlc.low,
            high=ohlc.high,
        )
