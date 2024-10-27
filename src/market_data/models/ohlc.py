from datetime import timedelta
from typing import ClassVar

from django.conf import settings
from django.db import models

from market_data.models.instrument import Instrument


class Ohlc(models.Model):
    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.PROTECT,
        related_name="ohlc_list",
    )

    open = models.DecimalField(max_digits=32, decimal_places=settings.DEFAULT_PRICE_DECIMAL_PLACES)
    close = models.DecimalField(max_digits=32, decimal_places=settings.DEFAULT_PRICE_DECIMAL_PLACES)
    low = models.DecimalField(max_digits=32, decimal_places=settings.DEFAULT_PRICE_DECIMAL_PLACES)
    high = models.DecimalField(max_digits=32, decimal_places=settings.DEFAULT_PRICE_DECIMAL_PLACES)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        """Meta."""

        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["instrument", "start_time", "end_time"],
                name="unique_ohlc",
            ),
        ]

    @property
    def interval(self) -> timedelta:
        return self.end_time - self.start_time
