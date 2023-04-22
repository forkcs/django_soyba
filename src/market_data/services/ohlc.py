from collections.abc import Sequence

from market_data import models


def create_or_update_ohlc_seq(ohlc_seq: Sequence[models.OHLC], batch_size: int = None) -> None:
    update_fields = [
        'open',
        'close',
        'low',
        'high',
    ]
    unique_fields = ['instrument', 'start_time', 'end_time']

    for ohlc in ohlc_seq:
        ohlc.full_clean()

    models.OHLC.objects.bulk_create(
        ohlc_seq,
        update_conflicts=True,
        update_fields=update_fields,
        unique_fields=unique_fields,
        batch_size=batch_size,
    )
