from enum import Enum

from pydantic import BaseModel


class SerialSendConfig(BaseModel):
    class SendMode(Enum):
        str = 'str'
        hex = 'hex'

    class AppendMode(Enum):
        none = 'none'
        r = 'r'
        n = 'n'
        rn = 'rn'

    send_mode: SendMode
    append_mode: AppendMode
