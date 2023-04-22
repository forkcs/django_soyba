from datetime import datetime
from unittest.mock import patch

from data_sources.api_interfaces.bybit.interface import BybitInterface
from data_sources.api_interfaces.schema import OHLC, Timeframe


class TestGetOHLC:
    def test_returns_valid_ohlc(
        self,
        ohlc_tuple: tuple[OHLC, ...],
        start_time: datetime,
        open: float,
        high: float,
        low: float,
        close: float,
        end_time: datetime,
    ):
        assert len(ohlc_tuple) == 1

        ohlc = ohlc_tuple[0]
        assert ohlc.open == open
        assert ohlc.high == high
        assert ohlc.low == low
        assert ohlc.close == close
        assert ohlc.start_time == start_time
        assert ohlc.end_time == end_time


class TestGetAvailableInstruments:
    def test_returns_only_available_instruments(
        self, available_instruments: tuple[str, ...], raw_available_instruments: dict
    ):
        with patch("pybit.unified_trading.HTTP.get_instruments_info") as get_instruments_info:
            get_instruments_info.return_value = raw_available_instruments
            instruments = BybitInterface().get_available_instruments()
            assert instruments == available_instruments


class TestGetAvailableTimeframes:
    def test_returns_hardcoded_tuple(self, available_timeframes: tuple[Timeframe, ...]):
        assert BybitInterface().get_available_timeframes() == available_timeframes
