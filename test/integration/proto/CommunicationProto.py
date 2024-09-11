import json
import struct

class CommunicationProtobuf:

    PAYLOAD_SIZE = 256
    PROTO_NO_ERROR = 0
    PROTO_INVAL_PTR = -1
    PROTO_OVERFLOW = -2
    PROTO_INVAL_SIZE = -3
    PROTO_INVAL_TYPE = -4
    PROTO_INVAL_JSON_PARSE = -5
    PROTO_INVAL_JSON_KEY = -6
    PROTO_INVAL_JSON_VALUE = -7

    def __init__(self):
        self._command = 0
        self._address = 0
        self._memory_area = 0
        self._recv_memory_area = 0
        self._payload = ""

    def get_command(self):
        return self._command

    def get_address(self):
        return self._address

    def get_memory_area(self):
        return self._memory_area

    def get_recv_memory_area(self):
        return self._recv_memory_area

    def get_payload(self):
        return self._payload

    def update_command(self, value):
        if isinstance(value, int):        
            self._command = value
            return self.PROTO_NO_ERROR

        return self.PROTO_INVAL_TYPE

    def update_address(self, value):
        if isinstance(value, int):        
            self._address = value
            return self.PROTO_NO_ERROR

        return self.PROTO_INVAL_TYPE

    def update_memory_area(self, value):
        if isinstance(value, int):        
            self._memory_area = value
            return self.PROTO_NO_ERROR

        return self.PROTO_INVAL_TYPE

    def update_recv_memory_area(self, value):
        if isinstance(value, int):        
            self._recv_memory_area = value
            return self.PROTO_NO_ERROR

        return self.PROTO_INVAL_TYPE

    def update_payload(self, value):
        if value is None:
            return self.PROTO_INVAL_PTR
        if not isinstance(value, str):
            return self.PROTO_INVAL_TYPE
        value_length = len(value)
        if value_length == 0 or self.PAYLOAD_SIZE == 0:
            return self.PROTO_OVERFLOW
        if value_length > self.PAYLOAD_SIZE:
            return self.PROTO_INVAL_SIZE
        self._payload = value
        return self.PROTO_NO_ERROR # Error in the protobuf generation!

    def serialize(self, out_buffer):
        if out_buffer is None:
            return 0

        data_position = 0

        out_buffer[data_position] = struct.pack('B', struct.calcsize('B'))[0]
        data_position += 1
        struct.pack_into('B', out_buffer, data_position, self._command)
        data_position += struct.calcsize('B')

        out_buffer[data_position] = struct.pack('H', struct.calcsize('H'))[0]
        data_position += 1
        struct.pack_into('H', out_buffer, data_position, self._address)
        data_position += struct.calcsize('H')

        out_buffer[data_position] = struct.pack('B', struct.calcsize('B'))[0]
        data_position += 1
        struct.pack_into('B', out_buffer, data_position, self._memory_area)
        data_position += struct.calcsize('B')

        out_buffer[data_position] = struct.pack('B', struct.calcsize('B'))[0]
        data_position += 1
        struct.pack_into('B', out_buffer, data_position, self._recv_memory_area)
        data_position += struct.calcsize('B')

        length = len(self._payload)
        out_buffer[data_position] = length
        data_position += 1
        out_buffer[data_position:data_position + length] = self._payload.encode('utf-8')
        data_position += length

        return data_position

    def deserialize(self, data):
        try:
            data_position = 0

            self.command_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self._command = struct.unpack_from('B', data, data_position)[0]
            data_position += self.command_size

            self.address_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self._address = struct.unpack_from('H', data, data_position)[0]
            data_position += self.address_size

            self.memory_area_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self._memory_area = struct.unpack_from('B', data, data_position)[0]
            data_position += self.memory_area_size

            self.recv_memory_area_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self._recv_memory_area = struct.unpack_from('B', data, data_position)[0]
            data_position += self.recv_memory_area_size

            self.payload_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self._payload = struct.unpack_from(
                '{}s'.format(self.payload_size),
                data,
                data_position
            )[0].decode('utf-8')
            data_position += self.payload_size

            return self.PROTO_NO_ERROR
        except Exception:
            return self.PROTO_INVAL_PTR

    def serialize_json(self, out_buffer, out_buffer_size):
        if out_buffer is None:
            return 0

        # Create a dictionary with the fields
        data = {
            "command": self._command,
            "address": self._address,
            "memory_area": self._memory_area,
            "recv_memory_area": self._recv_memory_area,
            "payload": self._payload
        }
        json_data = json.dumps(data)

        if len(json_data) > out_buffer_size:
            return 0

        out_buffer[:len(json_data)] = json_data.encode('utf-8')

        return len(json_data)

    def deserialize_json(self, in_buffer):
        if in_buffer is None:
            return self.PROTO_INVAL_PTR

        try:
            json_str = in_buffer.decode('utf-8')
            data = json.loads(json_str.split('\x00')[0])
            if "command" not in data:
                return self.PROTO_INVAL_JSON_KEY
            if "address" not in data:
                return self.PROTO_INVAL_JSON_KEY
            if "memory_area" not in data:
                return self.PROTO_INVAL_JSON_KEY
            if "recv_memory_area" not in data:
                return self.PROTO_INVAL_JSON_KEY
            if "payload" not in data:
                return self.PROTO_INVAL_JSON_KEY
            if self.update_command(data["command"]) != self.PROTO_NO_ERROR:
                return self.PROTO_INVAL_JSON_VALUE
            if self.update_address(data["address"]) != self.PROTO_NO_ERROR:
                return self.PROTO_INVAL_JSON_VALUE
            if self.update_memory_area(data["memory_area"]) != self.PROTO_NO_ERROR:
                return self.PROTO_INVAL_JSON_VALUE
            if self.update_recv_memory_area(data["recv_memory_area"]) != self.PROTO_NO_ERROR:
                return self.PROTO_INVAL_JSON_VALUE
            if self.update_payload(data["payload"]) != self.PROTO_NO_ERROR:
                return self.PROTO_INVAL_JSON_VALUE
            return self.PROTO_NO_ERROR
        except json.JSONDecodeError:
            return self.PROTO_INVAL_JSON_PARSE
