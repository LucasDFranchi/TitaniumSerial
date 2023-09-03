import pytest

from src.message_builder import MessageBuilder

@pytest.fixture
def message_object():
    _memory_area = b'\x00'
    _command = b'\x57'
    _data = b'\x01\x02\x03\x04\x05\x06\x07'
    obj = MessageBuilder.set_command(_command).set_memory_area(
        _memory_area).set_data(_data).build()
    
    yield obj

def test_builder(message_object):
    assert message_object is not None

def test_crc(message_object):
    _expected_crc = b'\x8E\x89\xD8\xC0'
    assert _expected_crc == message_object.crc

def test_byte_stream(message_object):
    _expected_byte_stream = b'\x00\x00\x07\x57\x00\x01\x02\x03\x04\x05\x06\x07\x8E\x89\xD8\xC0\x03'