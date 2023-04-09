from datetime import datetime
from decimal import Decimal

from pytest_mock import MockerFixture

from data_sources.api_interfaces.kraken.interface import KrakenInterface
from data_sources.api_interfaces.kraken.types import KrakenOHLC
from data_sources.api_interfaces.schema import Timeframe, TimeframeUnit


def test_kraken_get_ohlc_returns_valid_ohlc(mocker: MockerFixture) -> None:
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
