import time
import os
import sys

# Get the current script directory (test/)
script_dir = os.path.dirname(os.path.realpath(__file__))

# Get the parent directory (project_root/)
project_root = os.path.dirname(script_dir)

# Add project_root to the Python path
sys.path.append(project_root)

from src.serial_builder import SerialBuilder
from src.message_builder import MessageBuilder
from src.constants import MessageCommands, MessageAreas

def stress_test():
    com_port = "COM3"
    baudrate = 115200

    serial = (SerialBuilder.read_configuration()
                            .update_port(com_port)
                            .update_baudrate(baudrate)
                            .build())
    
    serial.open_serial_port()
    serial.flush()
    
    for i in range(1024):
        data_command = b'\xFF' * i

        message = (MessageBuilder.set_memory_area(MessageAreas.DISPLAY)
                            .set_command(MessageCommands.WRITE)
                            .set_data(data_command)
                            .build())
        
        serial.send_byte_stream(message.byte_stream)

        time.sleep(0.2)

    serial.close_serial_port()

stress_test()