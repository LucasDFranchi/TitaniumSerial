from enum import Enum

class MessageBounds(Enum):
    START_BYTE = b'\x02'
    END_BYTE = b'\x03'

class MessageCommands(Enum):
    READ = b'\x52'
    WRITE = b'\x57'

class MessageAreas(Enum):
    DISPLAY = b'\x01'
    SSID = b'\x02'
    PASSWORD = b'\x03'