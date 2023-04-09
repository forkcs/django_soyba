from typing import TypeAlias

KrakenOHLC: TypeAlias = tuple[int, str, str, str, str, str, str, int]

KrakenInstrument: TypeAlias = dict[str, str | int | float]
