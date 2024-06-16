from enum import Enum


class MessageBounds:
    START_BYTE = b'\x02'
    END_BYTE = b'\x03'


class MessageCommands:
    ACK = b'\x41'
    RESPONSE = b'\x45'
    READ = b'\x52'
    WRITE = b'\x57'


class MessageAreas:
    DISPLAY = b'\x00'
    SSID = b'\x01'
    PASSWORD = b'\x02'
    CONNECTION = b'\x03'
    LORA_WRITE = b'\x04'
    LORA_READ = b'\x05'
