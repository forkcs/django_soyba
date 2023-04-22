from datetime import datetime
from decimal import Decimal
from unittest import mock

from hypothesis import given
from hypothesis import strategies as st
from pytest_mock import MockerFixture

from data_sources.api_interfaces.binance.interface import BinanceInterface
from data_sources.api_interfaces.schema import OHLC, Timeframe, TimeframeUnit


def test_get_ohlc_returns_valid_ohlc(mocker: MockerFixture) -> None:
    klines_mock = mocker.patch("binance.spot.Spot.klines")
    klines_mock.return_value = (
        (
            start_time := 1499040000000,
            open_ := "0.01634790",
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

    assert ohlc.open.compare(Decimal(open_)) == 0
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


ohlc_strategy = st.tuples(
    st.datetimes().map(lambda dt: int(dt.timestamp() * 1000)),
    st.decimals(allow_nan=False, allow_infinity=False, min_value=0).map(str),
    st.decimals(allow_nan=False, allow_infinity=False, min_value=0).map(str),
    st.decimals(allow_nan=False, allow_infinity=False, min_value=0).map(str),
    st.decimals(allow_nan=False, allow_infinity=False, min_value=0).map(str),
    st.decimals(allow_nan=False, allow_infinity=False, min_value=0).map(str),
    st.datetimes().map(lambda dt: int(dt.timestamp() * 1000)),
    st.decimals(allow_nan=False, allow_infinity=False, min_value=0).map(str),
    st.integers(min_value=0),
    st.decimals(allow_nan=False, allow_infinity=False, min_value=0).map(str),
    st.decimals(allow_nan=False, allow_infinity=False, min_value=0).map(str),
    st.just('0'),
).map(list)


@given(
    raw_ohlc_list=st.lists(ohlc_strategy),
    symbol=st.from_regex(r'[A-Z_0-9]{2,10}'),
    timeframe=st.builds(Timeframe, count=st.integers(min_value=1), unit=st.sampled_from(TimeframeUnit)),
    count=st.integers(),
    start_datetime=st.datetimes(),
)
def test_get_ohlc(raw_ohlc_list: list[list], symbol: str, timeframe: Timeframe, count: int, start_datetime: datetime):
    with mock.patch('binance.spot.Spot.klines') as klines_mock:
        klines_mock.return_value = raw_ohlc_list

        ohlc_list = BinanceInterface().get_ohlc(
            symbol=symbol,
            timeframe=timeframe,
            count=count,
            start_datetime=start_datetime,
        )

        assert len(ohlc_list) == len(raw_ohlc_list)

        for ohlc, raw_ohlc in zip(ohlc_list, raw_ohlc_list):
            assert isinstance(ohlc, OHLC)

            assert ohlc.open == Decimal(raw_ohlc[1])
            assert ohlc.high == Decimal(raw_ohlc[2])
            assert ohlc.low == Decimal(raw_ohlc[3])
            assert ohlc.close == Decimal(raw_ohlc[4])
            assert ohlc.start_time == datetime.fromtimestamp(raw_ohlc[0] / 1000)
            assert ohlc.end_time == datetime.fromtimestamp(raw_ohlc[6] / 1000)
