from django.db import models

from data_sources.models import MarketDataSource


class Instrument(models.Model):
    symbol = models.CharField(max_length=255)
    market_data_source = models.ForeignKey(
        MarketDataSource,
        on_delete=models.PROTECT,
        related_name='instruments',
    )
