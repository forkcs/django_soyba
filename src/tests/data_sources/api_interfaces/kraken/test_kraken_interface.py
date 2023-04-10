from datetime import datetime
from decimal import Decimal

from pytest_mock import MockerFixture

from data_sources.api_interfaces.kraken.interface import KrakenInterface
from data_sources.api_interfaces.kraken.types import KrakenOHLC
from data_sources.api_interfaces.schema import Timeframe, TimeframeUnit


def test_get_ohlc_returns_valid_ohlc(mocker: MockerFixture) -> None:
    get_ohlc = mocker.patch("kraken.spot.Market.get_ohlc")
    return_value: dict[str, list[KrakenOHLC]] = {
        "XXBTCUTCBOBS": [
            (
                start_time := 1680997440,
                open := "27956.3",
                high := "27958.1",
                low := "27956.3",
                close := "27956.6",
                "27956.7",
                "0.04109108",
                13,
            )
        ],
    }
    get_ohlc.return_value = return_value

    ohlc_tuple = KrakenInterface().get_ohlc(
        symbol='BTCUTCBOBS', count=1, timeframe=Timeframe(1, TimeframeUnit.SECOND), start_datetime=datetime.now()
    )
    assert len(ohlc_tuple) == 1
    ohlc = ohlc_tuple[0]

    assert ohlc.open.compare(Decimal(open)) == 0
    assert ohlc.high.compare(Decimal(high)) == 0
    assert ohlc.low.compare(Decimal(low)) == 0
    assert ohlc.close.compare(Decimal(close)) == 0
    assert ohlc.start_time == datetime.fromtimestamp(start_time)


def test_get_available_timeframes_returns_hardcoded_tuple() -> None:
    timeframes = KrakenInterface().get_available_timeframes()
    assert timeframes == (
        Timeframe(count=1, unit=TimeframeUnit.MINUTE),
        Timeframe(count=5, unit=TimeframeUnit.MINUTE),
        Timeframe(count=15, unit=TimeframeUnit.MINUTE),
        Timeframe(count=60, unit=TimeframeUnit.MINUTE),
        Timeframe(count=240, unit=TimeframeUnit.MINUTE),
        Timeframe(count=1440, unit=TimeframeUnit.MINUTE),
        Timeframe(count=10080, unit=TimeframeUnit.MINUTE),
        Timeframe(count=21600, unit=TimeframeUnit.MINUTE),
    )


def test_get_available_instruments_returns_available_instrument_if_there_is_one(mocker: MockerFixture) -> None:
    get_instruments = mocker.patch("kraken.spot.Market.get_assets")
    get_instruments.return_value = {
        (symbol := "XBTUSD"): {"status": "enabled"},
        "BTCUSDT": {"status": "disabled"},
    }

    instruments: tuple[str] = tuple(KrakenInterface().get_available_instruments())
    assert len(instruments) == 1
    assert instruments[0] == symbol


def test_get_available_instruments_returns_multiple_available_instruments(mocker: MockerFixture) -> None:
    get_instruments = mocker.patch("kraken.spot.Market.get_assets")
    get_instruments.return_value = {
        (symbol1 := "XBTUSD"): {"status": "enabled"},
        "BTCUSDT": {"status": "disabled"},
        (symbol2 := "ETHBTC"): {"status": "enabled"},
    }

    instruments: tuple[str] = tuple(KrakenInterface().get_available_instruments())
    assert len(instruments) == 2
    assert instruments[0] == symbol1
    assert instruments[1] == symbol2
