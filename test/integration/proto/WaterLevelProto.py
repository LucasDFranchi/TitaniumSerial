import json
import struct

class WaterLevelProtobuf:

    PROTO_NO_ERROR = 0
    PROTO_INVAL_PTR = -1
    PROTO_OVERFLOW = -2
    PROTO_INVAL_SIZE = -3
    PROTO_INVAL_TYPE = -4
    PROTO_INVAL_JSON_PARSE = -5
    PROTO_INVAL_JSON_KEY = -6
    PROTO_INVAL_JSON_VALUE = -7

    def __init__(self):
        self._timestamp = 0
        self._value = 0

    def get_timestamp(self):
        return self._timestamp

    def get_value(self):
        return self._value

    def update_timestamp(self, value):
        if isinstance(value, int):        
            self._timestamp = value
            return self.PROTO_NO_ERROR

        return self.PROTO_INVAL_TYPE

    def update_value(self, value):
        if isinstance(value, int):        
            self._value = value
            return self.PROTO_NO_ERROR

        return self.PROTO_INVAL_TYPE

    def serialize(self, out_buffer):
        if out_buffer is None:
            return 0

        data_position = 0

        out_buffer[data_position] = struct.pack('Q', struct.calcsize('Q'))[0]
        data_position += 1
        struct.pack_into('Q', out_buffer, data_position, self._timestamp)
        data_position += struct.calcsize('Q')

        out_buffer[data_position] = struct.pack('I', struct.calcsize('I'))[0]
        data_position += 1
        struct.pack_into('I', out_buffer, data_position, self._value)
        data_position += struct.calcsize('I')

        return data_position

    def deserialize(self, data):
        try:
            data_position = 0

            self.timestamp_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self._timestamp = struct.unpack_from('Q', data, data_position)[0]
            data_position += self.timestamp_size

            self.value_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self._value = struct.unpack_from('I', data, data_position)[0]
            data_position += self.value_size

            return self.PROTO_NO_ERROR
        except Exception:
            return self.PROTO_INVAL_PTR

    def serialize_json(self, out_buffer, out_buffer_size):
        if out_buffer is None:
            return 0

        # Create a dictionary with the fields
        data = {
            "timestamp": self._timestamp,
            "value": self._value
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
            if "timestamp" not in data:
                return self.PROTO_INVAL_JSON_KEY
            if "value" not in data:
                return self.PROTO_INVAL_JSON_KEY
            if self.update_timestamp(data["timestamp"]) != self.PROTO_NO_ERROR:
                return self.PROTO_INVAL_JSON_VALUE
            if self.update_value(data["value"]) != self.PROTO_NO_ERROR:
                return self.PROTO_INVAL_JSON_VALUE
            return self.PROTO_NO_ERROR
        except json.JSONDecodeError:
            return self.PROTO_INVAL_JSON_PARSE
