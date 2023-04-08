from django.db import models


class MarketDataSource(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_market_data_source_name',
            ),
        ]
