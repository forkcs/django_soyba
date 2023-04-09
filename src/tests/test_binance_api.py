from datetime import datetime
from decimal import Decimal

from pytest_mock import MockerFixture

from data_sources.api_interfaces.binance.interface import BinanceInterface
from data_sources.api_interfaces.schema import OHLC, Timeframe, TimeframeUnit


def test_binance_get_ohlc_returns_valid_ohlc(mocker: MockerFixture) -> None:
    klines_mock = mocker.patch("binance.spot.Spot.klines")
    klines_mock.return_value = (
        (
            1499040000000,
            "0.01634790",
            "0.80000000",
            "0.01575800",
            "0.01577100",
            "148976.11427815",
            1499644799999,
            "2434.19055334",
            308,
            "1756.87402397",
            "28.46694368",
            "0",
        ),
    )

    ohlc_tuple = BinanceInterface().get_ohlc(
        symbol='XBTBOBS', timeframe=Timeframe(1, TimeframeUnit.SECOND), count=1, start_datetime=datetime.now()
    )

    assert len(ohlc_tuple) == 1
    ohlc: OHLC = ohlc_tuple[0]

    assert Decimal.compare(ohlc.open, Decimal("0.01634790")) == 0
    assert Decimal.compare(ohlc.high, Decimal("0.80000000")) == 0
    assert Decimal.compare(ohlc.low, Decimal("0.01575800")) == 0
    assert Decimal.compare(ohlc.close, Decimal("0.01577100")) == 0
    assert ohlc.start_time == datetime.fromtimestamp(1499040000000 / 1000)
    assert ohlc.end_time == datetime.fromtimestamp(1499644799999 / 1000)
