import json
from titanium_pb2 import NetworkCredentials, NetworkInformation, BrokerConfig
from titanium_pb2 import MemoryAreas

class ProtobufFactory:
    def __init__(self, json_file):
        self.json_file = json_file
        
        self._protobufs_dict = {
            0: NetworkCredentials,
            1: NetworkInformation,
            2: BrokerConfig,
        }

    def load_config_from_json(self):
        with open(self.json_file, 'r') as file:
            data = json.load(file)

        memory_area = data.get("memory_area")
        protobuf = self._protobufs_dict.get(memory_area)()
        
        payload_dict = data.get("payload")
        
        for key, value in payload_dict.items():
            setattr(protobuf, key, value)
        
        return protobuf