from typing import TypeAlias

BybitOHLC: TypeAlias = tuple[
    str,  # start_time
    str,  # open
    str,  # high
    str,  # low
    str,  # close
    str,  # end_time
    str,  # volume
]
