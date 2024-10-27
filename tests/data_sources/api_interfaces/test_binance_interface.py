from datetime import datetime
from decimal import Decimal
from unittest import mock

from hypothesis import assume, given
from hypothesis import strategies as st
from pytest_mock import MockerFixture

from django_soyba.data_sources.api_interfaces.binance.interface import BinanceInterface
from django_soyba.data_sources.api_interfaces.schema import Ohlc, Timeframe, TimeframeUnit


class TestGetOhlc:
    def test_get_ohlc_returns_valid_ohlc(self, mocker: MockerFixture):
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
            symbol="XBTBOBS",
            timeframe=Timeframe(1, TimeframeUnit.SECOND),
            count=1,
            start_datetime=datetime.now(),
        )
        expected_ohlc = Ohlc(
            open=Decimal(open),
            high=Decimal(high),
            low=Decimal(low),
            close=Decimal(close),
            start_time=datetime.fromtimestamp(start_time / 1000),
            end_time=datetime.fromtimestamp(end_time / 1000),
        )

        assert ohlc_tuple == (expected_ohlc,)


class TestGetAvailableTimeframes:
    def test(self):
        timeframes = BinanceInterface().get_available_timeframes()
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

    def test_returns_one_available_instrument(self, mocker: MockerFixture):
        get_exchange_info = mocker.patch("binance.spot.Spot.exchange_info")
        get_exchange_info.return_value = {
            "symbols": [
                {"symbol": (symbol := "BTCUSDT"), "status": "TRADING"},
            ],
        }

        instruments = BinanceInterface().get_available_instruments()
        assert instruments == (symbol,)

    def test_returns_all_when_all_are_insruments(self, mocker: MockerFixture):
        get_exchange_info = mocker.patch("binance.spot.Spot.exchange_info")
        get_exchange_info.return_value = {
            "symbols": [
                {"symbol": (symbol0 := "BTCUSDT"), "status": "TRADING"},
                {"symbol": (symbol1 := "TRXBTC"), "status": "TRADING"},
                {"symbol": (symbol2 := "ETHBTC"), "status": "TRADING"},
            ],
        }
        expected_instruments = (symbol0, symbol1, symbol2)

        instruments = BinanceInterface().get_available_instruments()
        assert instruments == expected_instruments

    def test_no_available_instruments(self, mocker: MockerFixture):
        get_exchange_info = mocker.patch("binance.spot.Spot.exchange_info")
        get_exchange_info.return_value = {
            "symbols": [
                {"symbol": "BTCUSDT", "status": "NOT-TRADING"},
                {"symbol": "TRXBTC", "status": "SHISHPING"},
                {"symbol": "ETHBTC", "status": "ZAZOYBING"},
            ],
        }

        instruments = BinanceInterface().get_available_instruments()
        assert len(instruments) == 0

    def test_returns_available_instrument_when_others_are_unavailable(self, mocker: MockerFixture):
        get_exchange_info = mocker.patch("binance.spot.Spot.exchange_info")
        get_exchange_info.return_value = {
            "symbols": [
                {"symbol": (symbol := "BTCUSDT"), "status": "TRADING"},
                {"symbol": "TRXBTC", "status": "SHISHPING"},
                {"symbol": "ETHBTC", "status": "ZAZOYBING"},
            ],
        }
        expected_instruments = (symbol,)
        instruments = BinanceInterface().get_available_instruments()
        assert instruments == expected_instruments


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
    st.just("0"),
).map(list)


@given(
    raw_ohlc_list=st.lists(ohlc_strategy),
    symbol=st.from_regex(r"[A-Z_0-9]{2,10}"),
    timeframe=st.builds(Timeframe, count=st.integers(min_value=1, max_value=400), unit=st.sampled_from(TimeframeUnit)),
    count=st.integers(max_value=1_000_000),
    start_datetime=st.datetimes(),
)
def test_get_ohlc(raw_ohlc_list: list[list], symbol: str, timeframe: Timeframe, count: int, start_datetime: datetime):
    assume(count <= len(raw_ohlc_list))

    with mock.patch("binance.spot.Spot.klines") as klines_mock:
        klines_mock.return_value = raw_ohlc_list

        ohlc_list = BinanceInterface().get_ohlc(
            symbol=symbol,
            timeframe=timeframe,
            count=count,
            start_datetime=start_datetime,
        )

        assert len(ohlc_list) == max(count, 0)

        for ohlc, raw_ohlc in zip(ohlc_list, raw_ohlc_list):
            expected_ohlc = Ohlc(
                open=raw_ohlc[1],
                high=raw_ohlc[2],
                low=raw_ohlc[3],
                close=raw_ohlc[4],
                start_time=datetime.fromtimestamp(raw_ohlc[0] / 1000),
                end_time=datetime.fromtimestamp(raw_ohlc[6] / 1000),
            )
            assert ohlc == expected_ohlc
