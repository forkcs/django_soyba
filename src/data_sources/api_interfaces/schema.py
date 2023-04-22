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
    end_time: datetime


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
        timedelta_by_unit = {
            TimeframeUnit.SECOND: timedelta(seconds=self.count),
            TimeframeUnit.MINUTE: timedelta(minutes=self.count),
            TimeframeUnit.HOUR: timedelta(hours=self.count),
            TimeframeUnit.DAY: timedelta(days=self.count),
            TimeframeUnit.WEEK: timedelta(days=self.count * 7),
            TimeframeUnit.MONTH: timedelta(days=self.count * 30),
            TimeframeUnit.YEAR: timedelta(days=self.count * 365),
        }

        return timedelta_by_unit[self.unit]

    def __lt__(self, other):
        return self.interval < other.interval
