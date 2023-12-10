import time

from src.serial_builder import SerialBuilder
from src.message_builder import MessageBuilder
from src.constants import MessageCommands, MessageAreas

def stress_test():
    com_port = "COM3"
    baudrate = 230400

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

        time.sleep(0.1)

    serial.close_serial_port()

stress_test()