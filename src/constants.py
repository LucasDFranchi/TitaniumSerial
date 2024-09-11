from enum import Enum

class MessageBounds(Enum):
    START_BYTE = 0x02
    END_BYTE = 0x03

class MessageCommands(Enum):
    INVALID_OPERATION = 0
    READ_COMMAND = 2
    WRITE_COMMAND = 4
    WRITE_SECURE_COMMAND = 102
    READ_SECURE_COMMAND = 103

# This should come from a file
class MessageAreas:
    DISPLAY = b"\x00"
    SSID = b"\x01"
    PASSWORD = b"\x02"
    CONNECTION = b"\x03"
    LORA_WRITE = b"\x04"
    LORA_READ = b"\x05"
