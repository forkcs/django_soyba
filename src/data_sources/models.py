from functools import reduce

from django.db import models


class MarketDataSourceChoices(models.TextChoices):
    BINANCE = 'binance', 'Binance'
    KRAKEN = 'kraken', 'Kraken'
    BYBIT = 'bybit', 'Bybit'

    @property
    @classmethod
    def options(cls) -> tuple[str, ...]:
        return reduce(lambda tup, pair: tup + pair, MarketDataSourceChoices.choices)
