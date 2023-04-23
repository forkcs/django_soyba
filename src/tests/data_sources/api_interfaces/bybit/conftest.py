from datetime import datetime
from unittest.mock import patch

import pytest

from data_sources.api_interfaces.bybit.interface import BybitInterface
from data_sources.api_interfaces.schema import OHLC, Timeframe, TimeframeUnit


@pytest.fixture
def start_time() -> datetime:
    return datetime.fromtimestamp(1670608800)


@pytest.fixture
def timeframe() -> Timeframe:
    return Timeframe(count=1, unit=TimeframeUnit.SECOND)


@pytest.fixture
def end_time(start_time: datetime, timeframe: Timeframe) -> datetime:
    return start_time + timeframe.interval


@pytest.fixture
def open() -> float:
    return 17071


@pytest.fixture
def high() -> float:
    return 17073


@pytest.fixture
def low() -> float:
    return 17027


@pytest.fixture
def close() -> float:
    return 17055.5


@pytest.fixture
def raw_klines(start_time: datetime, open: float, high: float, low: float, close: float) -> dict:
    return {
        "result": {
            "list": [
                [
                    str(start_time.timestamp() * 1000),
                    str(open),
                    str(high),
                    str(low),
                    str(close),
                ],
            ],
        },
    }


@pytest.fixture
def ohlc_tuple(raw_klines: dict, start_time: datetime) -> tuple[OHLC, ...]:
    with patch("pybit.unified_trading.HTTP.get_kline") as get_kline:
        get_kline.return_value = raw_klines

        return BybitInterface().get_ohlc(
            symbol='BTCUSD', count=1, timeframe=Timeframe(count=1, unit=TimeframeUnit.SECOND), start_datetime=start_time
        )


@pytest.fixture
def raw_available_instruments() -> dict:
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


@pytest.fixture
def available_instruments() -> tuple[str, ...]:
    return ("BTCUSDT",)


@pytest.fixture
def available_timeframes() -> tuple[Timeframe, ...]:
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
