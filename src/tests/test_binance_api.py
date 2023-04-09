from datetime import datetime
from decimal import Decimal

from pytest_mock import MockerFixture

from data_sources.api_interfaces.binance.interface import BinanceInterface
from data_sources.api_interfaces.schema import OHLC, Timeframe, TimeframeUnit


def test_get_ohlc_returns_valid_ohlc(mocker: MockerFixture) -> None:
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


def test_get_available_timeframes_returns_hardcoded_tuple() -> None:
    """The very useful test btw"""
    timeframes: tuple[Timeframe] = tuple(BinanceInterface().get_available_timeframes())
    assert timeframes == (
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


def test_get_available_instruments_returns_one_available_instrument(mocker: MockerFixture) -> None:
    get_exchange_info = mocker.patch("binance.spot.Spot.exchange_info")
    get_exchange_info.return_value = {
        "symbols": [
            {"symbol": (symbol := "BTCUSDT"), "status": "TRADING"},
        ]
    }

    instruments: tuple[str] = tuple(BinanceInterface().get_available_instruments())
    assert len(instruments) == 1
    assert instruments[0] == symbol


def test_get_available_instruments_returns_all_when_all_are_insruments(mocker: MockerFixture) -> None:
    get_exchange_info = mocker.patch("binance.spot.Spot.exchange_info")
    get_exchange_info.return_value = {
        "symbols": [
            {"symbol": (symbol0 := "BTCUSDT"), "status": "TRADING"},
            {"symbol": (symbol1 := "TRXBTC"), "status": "TRADING"},
            {"symbol": (symbol2 := "ETHBTC"), "status": "TRADING"},
        ]
    }

    instruments: tuple[str] = tuple(BinanceInterface().get_available_instruments())
    assert len(instruments) == 3
    assert instruments[0] == symbol0
    assert instruments[1] == symbol1
    assert instruments[2] == symbol2


def test_get_available_instruments_returns_empty_when_no_available_instruments(mocker: MockerFixture) -> None:
    get_exchange_info = mocker.patch("binance.spot.Spot.exchange_info")
    get_exchange_info.return_value = {
        "symbols": [
            {"symbol": "BTCUSDT", "status": "NOT-TRADING"},
            {"symbol": "TRXBTC", "status": "SHISHPING"},
            {"symbol": "ETHBTC", "status": "ZAZOYBING"},
        ]
    }

    instruments: tuple[str] = tuple(BinanceInterface().get_available_instruments())
    assert len(instruments) == 0


def test_get_available_instruments_returns_one_available_instrument_when_others_are_unavailable(
    mocker: MockerFixture,
) -> None:
    get_exchange_info = mocker.patch("binance.spot.Spot.exchange_info")
    get_exchange_info.return_value = {
        "symbols": [
            {"symbol": (symbol := "BTCUSDT"), "status": "TRADING"},
            {"symbol": "TRXBTC", "status": "SHISHPING"},
            {"symbol": "ETHBTC", "status": "ZAZOYBING"},
        ]
    }

    instruments: tuple[str] = tuple(BinanceInterface().get_available_instruments())
    assert len(instruments) == 1
    assert instruments[0] == symbol
