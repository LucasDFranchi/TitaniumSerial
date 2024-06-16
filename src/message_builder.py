import binascii
import struct

from .constants import MessageBounds, MessageCommands


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
        if command == 'R':
            cls._command = MessageCommands.READ
        elif command == 'W':
            cls._command = MessageCommands.WRITE
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
            memory_area=cls._memory_area,
            data=cls._data,
        )

    class Message:
        def __init__(self, command, memory_area, data):
            self._start_byte = MessageBounds.START_BYTE
            self._end_byte = MessageBounds.END_BYTE
            self._command = command
            self._memory_area = memory_area
            self._data_length = len(data).to_bytes(2, byteorder="big")
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
                + self._data_length
                + self._command
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
            return struct.pack(">I", binascii.crc32(_byte_stream))