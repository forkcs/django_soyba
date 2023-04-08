from dataclasses import dataclass
from datetime import datetime
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
