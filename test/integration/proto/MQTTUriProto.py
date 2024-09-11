import json
import struct

class MQTTUriProtobuf:

    MQTT_URI_SIZE = 256
    PROTO_NO_ERROR = 0
    PROTO_INVAL_PTR = -1
    PROTO_OVERFLOW = -2
    PROTO_INVAL_SIZE = -3
    PROTO_INVAL_TYPE = -4
    PROTO_INVAL_JSON_PARSE = -5
    PROTO_INVAL_JSON_KEY = -6
    PROTO_INVAL_JSON_VALUE = -7

    def __init__(self):
        self._mqtt_uri = ""

    def get_mqtt_uri(self):
        return self._mqtt_uri

    def update_mqtt_uri(self, value):
        if value is None:
            return self.PROTO_INVAL_PTR
        if not isinstance(value, str):
            return self.PROTO_INVAL_TYPE
        value_length = len(value)
        if value_length == 0 or self.MQTT_URI_SIZE == 0:
            return self.PROTO_OVERFLOW
        if value_length > self.MQTT_URI_SIZE:
            return self.PROTO_INVAL_SIZE
        self._fourth_field = value
        return self.PROTO_NO_ERROR

    def serialize(self, out_buffer):
        if out_buffer is None:
            return 0

        data_position = 0

        length = len(self._mqtt_uri)
        out_buffer[data_position] = length
        data_position += 1
        out_buffer[data_position:data_position + length] = self._mqtt_uri.encode('utf-8')
        data_position += length

        return data_position

    def deserialize(self, data):
        try:
            data_position = 0

            self.mqtt_uri_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self._fourth_field = struct.unpack_from(
                '{}s'.format(self.mqtt_uri_size),
                data,
                data_position
            )[0].decode('utf-8')
            data_position += self.mqtt_uri_size

            return self.PROTO_NO_ERROR
        except Exception:
            return self.PROTO_INVAL_PTR

    def serialize_json(self, out_buffer, out_buffer_size):
        if out_buffer is None:
            return 0

        # Create a dictionary with the fields
        data = {
            "mqtt_uri": self._mqtt_uri
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
            if "mqtt_uri" not in data:
                return self.PROTO_INVAL_JSON_KEY
            if self.update_mqtt_uri(data["mqtt_uri"]) != self.PROTO_NO_ERROR:
                return self.PROTO_INVAL_JSON_VALUE
            return self.PROTO_NO_ERROR
        except json.JSONDecodeError:
            return self.PROTO_INVAL_JSON_PARSE
