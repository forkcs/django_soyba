from datetime import datetime
from decimal import Decimal

from pytest_mock import MockerFixture

from data_sources.api_interfaces.bybit.interface import BybitInterface
from data_sources.api_interfaces.schema import OHLC, Timeframe, TimeframeUnit


def test_get_ohlc_returns_valid_ohlc(mocker: MockerFixture):
    get_kline = mocker.patch("pybit.unified_trading.HTTP.get_kline")
    get_kline.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {
            "symbol": "BTCUSD",
            "category": "inverse",
            "list": [
                [
                    start_time := "1670608800000",
                    open := "17071",
                    high := "17073",
                    low := "17027",
                    close := "17055.5",
                    "268611",
                    "15.74462667",
                ],
            ],
        },
        "retExtInfo": {},
        "time": 1672025956592,
    }

    ohlc_tuple: tuple[OHLC] = BybitInterface().get_ohlc(
        symbol='BTCUSD',
        count=1,
        timeframe=Timeframe(count=1, unit=TimeframeUnit.SECOND),
        start_datetime=datetime.now(),
    )
    assert len(ohlc_tuple) == 1

    ohlc = ohlc_tuple[0]
    assert ohlc.open.compare(Decimal(open)) == 0
    assert ohlc.high.compare(Decimal(high)) == 0
    assert ohlc.low.compare(Decimal(low)) == 0
    assert ohlc.close.compare(Decimal(close)) == 0
    assert ohlc.start_time == datetime.fromtimestamp(float(start_time) / 1000)


def test_get_available_instruments_returns_only_available_instruments(mocker: MockerFixture):
    get_instruments_info = mocker.patch("pybit.unified_trading.HTTP.get_instruments_info")
    get_instruments_info.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {
            "category": "linear",
            "list": [
                {
                    "symbol": (symbol := "BTCUSDT"),
                    "contractType": "LinearPerpetual",
                    "status": "Trading",
                    "baseCoin": "BTC",
                    "quoteCoin": "USDT",
                    "launchTime": "1585526400000",
                    "deliveryTime": "0",
                    "deliveryFeeRate": "",
                    "priceScale": "2",
                    "leverageFilter": {"minLeverage": "1", "maxLeverage": "100.00", "leverageStep": "0.01"},
                    "priceFilter": {"minPrice": "0.50", "maxPrice": "999999.00", "tickSize": "0.50"},
                    "lotSizeFilter": {
                        "maxOrderQty": "100.000",
                        "minOrderQty": "0.001",
                        "qtyStep": "0.001",
                        "postOnlyMaxOrderQty": "1000.000",
                    },
                    "unifiedMarginTrade": True,
                    "fundingInterval": 480,
                    "settleCoin": "USDT",
                },
                {
                    "symbol": "XBTUSD",
                    "contractType": "LinearPerpetual",
                    "status": "Not-trading",
                    "baseCoin": "BTC",
                    "quoteCoin": "USDT",
                    "launchTime": "1585526400000",
                    "deliveryTime": "0",
                    "deliveryFeeRate": "",
                    "priceScale": "2",
                    "leverageFilter": {"minLeverage": "1", "maxLeverage": "100.00", "leverageStep": "0.01"},
                    "priceFilter": {"minPrice": "0.50", "maxPrice": "999999.00", "tickSize": "0.50"},
                    "lotSizeFilter": {
                        "maxOrderQty": "100.000",
                        "minOrderQty": "0.001",
                        "qtyStep": "0.001",
                        "postOnlyMaxOrderQty": "1000.000",
                    },
                    "unifiedMarginTrade": True,
                    "fundingInterval": 480,
                    "settleCoin": "USDT",
                },
            ],
            "nextPageCursor": "",
        },
        "retExtInfo": {},
        "time": 1672712495660,
    }

    instruments: tuple[str, ...] = BybitInterface().get_available_instruments()
    assert instruments == (symbol,)


def test_get_available_timeframes_returns_hardcoded_tuple():
    timeframes = BybitInterface().get_available_timeframes()
    assert timeframes == (
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
