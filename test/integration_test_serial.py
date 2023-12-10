import time
import os
import sys
import yaml


# Get the current script directory (test/)
script_dir = os.path.dirname(os.path.realpath(__file__))

# Get the parent directory (project_root/)
project_root = os.path.dirname(script_dir)

# Add project_root to the Python path
sys.path.append(project_root)

from src.serial_builder import SerialBuilder
from src.message_builder import MessageBuilder
from src.constants import MessageCommands


def integration_test_serial():
    com_port = "COM3"
    baudrate = 115200

    serial = (SerialBuilder.read_configuration()
                            .update_port(com_port)
                            .update_baudrate(baudrate)
                            .build())
    
    serial.open_serial_port()
    serial.flush()

    _clear_serial_start_up(serial)

    memory_areas_definitions = _import_areas_definition()
    for i in range(2):
        for _, value in memory_areas_definitions.items():

            random_bytes = os.urandom(value.get("size"))
            message = (MessageBuilder.set_memory_area(value.get("index").to_bytes(1, byteorder='big'))
                                    .set_command(MessageCommands.WRITE)
                                    .set_data(random_bytes)
                                    .build())
            serial.send_byte_stream(message.byte_stream)
            time.sleep(0.5)
            return_stream = serial.read_byte_stream()
            if (b"ACKOK" not in return_stream):
                print(return_stream)
                print(f"Error in Write {value.get('index')}")
                break
            
            message = (MessageBuilder.set_memory_area(value.get("index").to_bytes(1, byteorder='big'))
                                    .set_command(MessageCommands.READ)
                                    .set_data(random_bytes)
                                    .build())
            
            serial.send_byte_stream(message.byte_stream)
            time.sleep(0.5)
            return_stream = serial.read_byte_stream()
            if (random_bytes + b"ACKOK") != return_stream:
                print(f"Error in Read {value.get('index')}")
            else:
                print(f"Memory Area {value.get('index')} read and write succesfully!")
        
def _import_areas_definition():
    data = None

    with open("./assets/memory_areas.yaml", "r") as yaml_file:
        data = yaml.safe_load(yaml_file)

    return data

def _clear_serial_start_up(serial):
    time.sleep(5)
    serial.read_byte_stream()

integration_test_serial()