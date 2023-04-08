from django.db import models


class MarketDataSourceChoices(models.TextChoices):
    BINANCE = 'binance', 'Binance'
