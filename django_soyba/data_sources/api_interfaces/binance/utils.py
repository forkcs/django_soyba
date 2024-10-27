from data_sources.api_interfaces.schema import Timeframe


def format_binance_timeframe(timeframe: Timeframe) -> str:
    return f'{timeframe.count}{timeframe.unit.value}'
