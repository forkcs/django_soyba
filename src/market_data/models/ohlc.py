from django.conf import settings
from django.db import models

from market_data.models.instrument import Instrument


class OHLC(models.Model):
    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.PROTECT,
        related_name='ohlc_list',
    )

    open = models.DecimalField(max_digits=32, decimal_places=settings.DEFAULT_DECIMAL_PLACES)
    close = models.DecimalField(max_digits=32, decimal_places=settings.DEFAULT_DECIMAL_PLACES)
    low = models.DecimalField(max_digits=32, decimal_places=settings.DEFAULT_DECIMAL_PLACES)
    high = models.DecimalField(max_digits=32, decimal_places=settings.DEFAULT_DECIMAL_PLACES)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()