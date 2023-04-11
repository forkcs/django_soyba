from datetime import datetime
from decimal import Decimal

import pytest
from pytest_mock import MockerFixture

from data_sources.api_interfaces.bybit.interface import BybitInterface
from data_sources.api_interfaces.schema import OHLC, Timeframe, TimeframeUnit


class TestGetOHLC:
    @pytest.fixture
    def klines(self):
        return {
            "result": {
                "list": [
                    [
                        "1670608800000",
                        "17071",
                        "17073",
                        "17027",
                        "17055.5",
                        "268611",
                        "15.74462667",
                    ],
                ],
            },
            "time": 1672025956592,
        }

    def test_returns_valid_ohlc(self, mocker: MockerFixture, klines):
        get_kline = mocker.patch("pybit.unified_trading.HTTP.get_kline")
        get_kline.return_value = klines

        ohlc_tuple: tuple[OHLC] = BybitInterface().get_ohlc(
            symbol='BTCUSD',
            count=1,
            timeframe=Timeframe(count=1, unit=TimeframeUnit.SECOND),
            start_datetime=datetime.now(),
        )
        assert len(ohlc_tuple) == 1

        ohlc = ohlc_tuple[0]
        assert ohlc.open.compare(Decimal(17071)) == 0
        assert ohlc.high.compare(Decimal(17073)) == 0
        assert ohlc.low.compare(Decimal(17027)) == 0
        assert ohlc.close.compare(Decimal(17055.5)) == 0
        assert ohlc.start_time == datetime.fromtimestamp(float(1670608800000) / 1000)
        assert ohlc.end_time == datetime.fromtimestamp(float(1672025956592) / 1000)


class TestGetAvailableInstruments:
    @pytest.fixture
    def available_instruments(self):
        return {
            "result": {
                "list": [
                    {
                        "symbol": "BTCUSDT",
                        "status": "Trading",
                    },
                    {
                        "symbol": "XBTUSD",
                        "status": "Not-trading",
                    },
                ],
            },
        }

    def test_returns_only_available_instruments(self, mocker: MockerFixture, available_instruments):
        get_instruments_info = mocker.patch("pybit.unified_trading.HTTP.get_instruments_info")
        get_instruments_info.return_value = available_instruments

        instruments: tuple[str, ...] = BybitInterface().get_available_instruments()
        assert instruments == ("BTCUSDT",)


class TestGetAvailableTimeframes:
    @pytest.fixture
    def timeframes(self):
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

    def test_returns_hardcoded_tuple(self, timeframes):
        tf = BybitInterface().get_available_timeframes()
        assert tf == timeframes
