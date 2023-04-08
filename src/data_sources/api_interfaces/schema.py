from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum


@dataclass(frozen=True)
class OHLC:
    open: Decimal
    close: Decimal
    low: Decimal
    high: Decimal

    start_time: datetime
    end_time: datetime | None = None


class TimeframeUnit(Enum):
    SECOND = 's'
    MINUTE = 'm'
    HOUR = 'h'
    DAY = 'd'
    WEEK = 'w'
    MONTH = 'M'
    YEAR = 'y'


@dataclass(frozen=True)
class Timeframe:
    count: int
    unit: TimeframeUnit

    @property
    def interval(self) -> timedelta:
        if self.unit == TimeframeUnit.SECOND:
            return timedelta(seconds=self.count)
        elif self.unit == TimeframeUnit.MINUTE:
            return timedelta(minutes=self.count)
        elif self.unit == TimeframeUnit.HOUR:
            return timedelta(hours=self.count)
        elif self.unit == TimeframeUnit.DAY:
            return timedelta(days=self.count)
        elif self.unit == TimeframeUnit.WEEK:
            return timedelta(weeks=self.count)
        elif self.unit == TimeframeUnit.MONTH:
            return timedelta(days=self.count * 30)
        elif self.unit == TimeframeUnit.YEAR:
            return timedelta(days=self.count * 365)
