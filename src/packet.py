from .message_builder import MessageBuilder

import sys

class Packet:
    def __init__(self, memory_area, command, data):
        self.memory_area = memory_area
        self.command = command
        self.data = data

    @classmethod
    def from_byte_stream(cls, byte_stream):
        payload_length = int.from_bytes(byte_stream[1:3], byteorder='little')
        command = byte_stream[3]
        memory_area = byte_stream[4]
        payload = byte_stream[5:5+payload_length]
        
        message = (
            MessageBuilder.set_memory_area(memory_area)
            .set_command(chr(command))
            .set_data(payload)
            .build()
        )
        if payload_length != len(payload):
            return
        if byte_stream[:10+payload_length] == message.byte_stream:
            print(f"Received Data: {payload.decode("utf-8")}")
            
        return cls(memory_area, command, payload)