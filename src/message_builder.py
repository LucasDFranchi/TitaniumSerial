import binascii
import struct
import yaml

from .constants import MessageBounds

class MessageBuilder:
    @classmethod
    def set_command(cls, command):
        """
        Set the command for the message.

        Args:
            command (bytes): The command to set.

        Returns:
            cls: The class instance for method chaining.
        """
        cls._command = command
        return cls

    @classmethod    
    def set_memory_area(cls, memory_area):
        """
        Set the memory area for the message.

        Args:
            memory_area (bytes): The memory area to set.

        Returns:
            cls: The class instance for method chaining.
        """
        cls._memory_area = memory_area
        return cls
    
    @classmethod
    def set_data(cls, data):
        """
        Set the data for the message.

        Args:
            data (bytes): The data to set.

        Returns:
            cls: The class instance for method chaining.
        """
        cls._data = data
        return cls

    @classmethod
    def build(cls):
        """
        Build and return a message with the configured parameters.

        Returns:
            Message: An instance of the inner Message class.
        """
        return cls.Message(
            command=cls._command,
            memory_area=cls._memory_area,
            data=cls._data,
        )

    class Message:
        def __init__(self, command, memory_area, data):
            _APPEND_BYTE = b'\x00'

            _memory_area_size = self._get_message_size(memory_area)
            _not_null_size = len(data)

            self._start_byte = MessageBounds.START_BYTE
            self._end_byte = MessageBounds.END_BYTE
            self._command = command
            self._memory_area = memory_area
            self._data_length = _memory_area_size.to_bytes(2, byteorder='big')
            self._data = data + (_APPEND_BYTE * (_memory_area_size - _not_null_size))
            self._crc = self._calculate_crc()

        @property
        def crc(self):
            """
            Get the CRC checksum of the message.

            Returns:
                bytes: The CRC checksum as a bytes object.
            """
            return self._crc
        
        @property
        def byte_stream(self):
            """
            Get the entire message as a byte stream.

            Returns:
                bytes: The byte stream representing the message.
            """
            return self._start_byte + self._data_length + \
                self._command + self._memory_area + self._data + \
                self._crc + self._end_byte
        
        def _calculate_crc(self):
            """
            Calculate and return the CRC checksum of the message.

            Returns:
                bytes: The CRC checksum as a bytes object.
            """
            _byte_stream = self._start_byte + self._data_length + \
                self._command + self._memory_area + self._data
            return struct.pack(">I", binascii.crc32(_byte_stream))

        def _get_message_size(self, memory_area):
            _size = 0
            _converted_area = int.from_bytes(memory_area, byteorder='little')

            with open("./assets/memory_areas.yaml", "r") as yaml_file:
                data = yaml.safe_load(yaml_file)
                for key, entry in data.items():
                    if entry.get("index") == _converted_area:
                        _size = entry.get("size")

            return _size