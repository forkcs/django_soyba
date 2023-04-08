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

    @classmethod
    def construct(cls, spec: str) -> "Timeframe":
        if len(spec) == 0:
            raise ValueError("`spec` must contain integer and a TimeframeUnit specifier.")

        if spec[-1] not in TimeframeUnit:
            raise ValueError("`spec` last character must be a TimeframeUnit specifier.")

        try:
            int(spec[:-1])
        except:
            raise ValueError("`spec` must contain integer and a TimeframeUnit specifier.")

        return cls(count=int(spec[:-1]), unit=TimeframeUnit(spec[-1]))
