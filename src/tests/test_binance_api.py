from datetime import datetime
from decimal import Decimal

from pytest_mock import MockerFixture

from data_sources.api_interfaces.binance.interface import BinanceInterface
from data_sources.api_interfaces.schema import OHLC, Timeframe, TimeframeUnit


def test_binance_get_ohlc_returns_valid_ohlc(mocker: MockerFixture) -> None:
    klines_mock = mocker.patch("binance.spot.Spot.klines")
    klines_mock.return_value = (
        (
            start_time := 1499040000000,
            open := "0.01634790",
            high := "0.80000000",
            low := "0.01575800",
            close := "0.01577100",
            "148976.11427815",
            end_time := 1499644799999,
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

    assert ohlc.open.compare(Decimal(open)) == 0
    assert ohlc.high.compare(Decimal(high)) == 0
    assert ohlc.low.compare(Decimal(low)) == 0
    assert ohlc.close.compare(Decimal(close)) == 0
    assert ohlc.start_time == datetime.fromtimestamp(start_time / 1000)
    assert ohlc.end_time == datetime.fromtimestamp(end_time / 1000)
