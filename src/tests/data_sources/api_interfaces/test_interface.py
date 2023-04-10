from datetime import datetime
from decimal import Decimal
from unittest import mock

from hypothesis import given
from hypothesis import strategies as st

from data_sources.api_interfaces.binance.interface import BinanceInterface
from data_sources.api_interfaces.schema import OHLC, Timeframe, TimeframeUnit

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
