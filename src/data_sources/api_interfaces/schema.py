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
    def minutes(self) -> float:
        MINUTES_BY_UNIT = {
            TimeframeUnit.SECOND: 1/60,
            TimeframeUnit.MINUTE: 1,
            TimeframeUnit.HOUR: 60,
            TimeframeUnit.DAY: 24*60,
            TimeframeUnit.MONTH: 24*60*30,
            TimeframeUnit.YEAR: 24*60*365,
        }

        try:
            return self.count * MINUTES_BY_UNIT[self.unit]
        except KeyError:
            raise ValueError("Unknown TimeframeUnit value")

    @property
    def interval(self) -> timedelta:
        TIMEDELTA_BY_UNIT = {
            TimeframeUnit.SECOND: timedelta(seconds=self.count),
            TimeframeUnit.MINUTE: timedelta(minutes=self.count),
            TimeframeUnit.HOUR: timedelta(hours=self.count),
            TimeframeUnit.DAY: timedelta(days=self.count),
            TimeframeUnit.MONTH: timedelta(days=self.count * 30),
            TimeframeUnit.YEAR: timedelta(days=self.count * 365),
        }

        try:
            return TIMEDELTA_BY_UNIT[self.unit]
        except KeyError:
            raise ValueError("Unknown TimeframeUnit value")
