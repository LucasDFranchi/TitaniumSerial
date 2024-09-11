import json
import struct

class ConnectionStatusProtobuf:

    PROTO_NO_ERROR = 0
    PROTO_INVAL_PTR = -1
    PROTO_OVERFLOW = -2
    PROTO_INVAL_SIZE = -3
    PROTO_INVAL_TYPE = -4
    PROTO_INVAL_JSON_PARSE = -5
    PROTO_INVAL_JSON_KEY = -6
    PROTO_INVAL_JSON_VALUE = -7

    def __init__(self):
        self._ap_status = 0
        self._sta_status = 0

    def get_ap_status(self):
        return self._ap_status

    def get_sta_status(self):
        return self._sta_status

    def update_ap_status(self, value):
        if isinstance(value, int):        
            self._ap_status = value
            return self.PROTO_NO_ERROR

        return self.PROTO_INVAL_TYPE

    def update_sta_status(self, value):
        if isinstance(value, int):        
            self._sta_status = value
            return self.PROTO_NO_ERROR

        return self.PROTO_INVAL_TYPE

    def serialize(self, out_buffer):
        if out_buffer is None:
            return 0

        data_position = 0

        out_buffer[data_position] = struct.pack('B', struct.calcsize('B'))[0]
        data_position += 1
        struct.pack_into('B', out_buffer, data_position, self._ap_status)
        data_position += struct.calcsize('B')

        out_buffer[data_position] = struct.pack('B', struct.calcsize('B'))[0]
        data_position += 1
        struct.pack_into('B', out_buffer, data_position, self._sta_status)
        data_position += struct.calcsize('B')

        return data_position

    def deserialize(self, data):
        try:
            data_position = 0

            self.ap_status_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self._ap_status = struct.unpack_from('B', data, data_position)[0]
            data_position += self.ap_status_size

            self.sta_status_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self._sta_status = struct.unpack_from('B', data, data_position)[0]
            data_position += self.sta_status_size

            return self.PROTO_NO_ERROR
        except Exception:
            return self.PROTO_INVAL_PTR

    def serialize_json(self, out_buffer, out_buffer_size):
        if out_buffer is None:
            return 0

        # Create a dictionary with the fields
        data = {
            "ap_status": self._ap_status,
            "sta_status": self._sta_status
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
            if "ap_status" not in data:
                return self.PROTO_INVAL_JSON_KEY
            if "sta_status" not in data:
                return self.PROTO_INVAL_JSON_KEY
            if self.update_ap_status(data["ap_status"]) != self.PROTO_NO_ERROR:
                return self.PROTO_INVAL_JSON_VALUE
            if self.update_sta_status(data["sta_status"]) != self.PROTO_NO_ERROR:
                return self.PROTO_INVAL_JSON_VALUE
            return self.PROTO_NO_ERROR
        except json.JSONDecodeError:
            return self.PROTO_INVAL_JSON_PARSE
