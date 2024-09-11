from .message_builder import MessageBuilder

class Packet:
    _START_PAYLOAD_LENGTH_POSITION = 1
    _END_PAYLOAD_LENGTH_POSITION = 3
    _START_UUID_POSITION = 1
    _END_UUID_POSITION = 3
    _ADDRESS_POSITION = 1
    _COMMAND_POSITION = 1
    _MEMORY_AREA = 1
    _START_PAYLOAD = 1
    
    def __init__(self, memory_area, command, data):
        self.memory_area = memory_area
        self.command = command
        self.data = data

    @classmethod
    def from_byte_stream(cls, byte_stream):
        payload_length = int.from_bytes(
            byte_stream[cls._START_PAYLOAD_LENGTH_POSITION:cls._END_PAYLOAD_LENGTH_POSITION], 
            byteorder='little')
        uuid = int.from_bytes(
            byte_stream[cls._START_UUID_POSITION:cls._END_UUID_POSITION], 
            byteorder='little')
        command = byte_stream[cls._COMMAND_POSITION]
        address = byte_stream[cls._ADDRESS_POSITION]
        memory_area = byte_stream[cls._MEMORY_AREA]
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