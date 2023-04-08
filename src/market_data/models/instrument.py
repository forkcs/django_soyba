from django.db import models

from data_sources.models import MarketDataSourceChoices


class Instrument(models.Model):
    symbol = models.CharField(max_length=255)
    market_data_source = models.CharField(
        max_length=255,
        choices=MarketDataSourceChoices.choices,
    )
