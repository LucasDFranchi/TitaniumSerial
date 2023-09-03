import pytest

from src.serial_builder import SerialBuilder

@pytest.fixture
def serial_object():
    obj = SerialBuilder.build()
    
    yield obj

def test_builder(serial_object):
    assert serial_object is not None