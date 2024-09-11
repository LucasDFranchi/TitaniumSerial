import binascii
import os
import struct

from .constants import MessageBounds, MessageCommands

class MessageBuilder:
    _uuid = 0xFFFF
    
    @classmethod
    def set_address(cls, address):
        """
        Set the address for the message.

        Args:
            address (bytes): The address to set.

        Returns:
            cls: The class instance for method chaining.
        """
        if 0xFFFF > address > 0:
            cls._address = address
        return cls
    
    @classmethod
    def set_uuid(cls, uuid):
        """
        Set the uuid for the message.

        Args:
            uuid (bytes): The uuid to set.

        Returns:
            cls: The class instance for method chaining.
        """
        cls._uuid = uuid
        return cls
    
    @classmethod
    def set_command(cls, command):
        """
        Set the command for the message.

        Args:
            command (CommandType): The command to set.

        Returns:
            cls: The class instance for method chaining.
        """
        if isinstance(command, MessageCommands):
            cls._command = command
        else:
            raise ValueError("command must be an instance of CommandType Enum")
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
        cls._memory_area = memory_area.to_bytes(1, byteorder="big")
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
            address=cls._address,
            memory_area=cls._memory_area,
            data=cls._data,
            uuid=cls._uuid,
        )

    class Message:
        def __init__(self, command, address, memory_area, data, uuid = None):
            self._start_byte = MessageBounds.START_BYTE
            self._end_byte = MessageBounds.END_BYTE
            self._uuid = os.urandom(4) if uuid is None else uuid 
            self._command = command
            self._address = address
            self._memory_area = memory_area
            self._data_length = len(data).to_bytes(2, byteorder="little")
            self._data = data
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
            return (
                self._start_byte
                + self._uuid
                + self._data_length
                + self._command
                + self._address
                + self._memory_area
                + self._data
                + self._crc
                + self._end_byte
            )
            
        @property
        def byte_stream_str(self):
            """
            Get the entire message as a byte stream.

            Returns:
                bytes: The byte stream representing the message.
            """
            return [hex(x) for x in self.byte_stream]
            

        def _calculate_crc(self):
            """
            Calculate and return the CRC checksum of the message.

            Returns:
                bytes: The CRC checksum as a bytes object.
            """
            _byte_stream = (
                self._start_byte
                + self._data_length
                + self._command
                + self._memory_area
                + self._data
            )
            return struct.pack("<I", binascii.crc32(_byte_stream))