from .api_interfaces.base.interface import DataSourceInterface
from .api_interfaces.binance.interface import BinanceInterface

INTERFACE_BY_DATA_SOURCE_NAME = {
    'binance': BinanceInterface,
}


def get_interface_by_data_source_name(data_source_name: str) -> type[DataSourceInterface]:
    interface = INTERFACE_BY_DATA_SOURCE_NAME.get(data_source_name)

    if interface is not None:
        return interface

    raise ValueError(f'Unknown data source: {data_source_name}')
