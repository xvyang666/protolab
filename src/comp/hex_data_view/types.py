from datetime import datetime
from enum import Enum
from typing import NamedTuple


class HexViewDirection(Enum):
    RX = 'RX'
    TX = 'TX'


class HexViewRowData(NamedTuple):
    date_time: datetime
    bytes_data: bytes
    direction: HexViewDirection
