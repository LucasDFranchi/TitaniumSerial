import time

from src.serial_builder import SerialBuilder
from src.message_builder import MessageBuilder
from src.constants import MessageCommands, MessageAreas

def lora_test():
    titanium_lora_ping = {
        "port": "COM3",
        "baudrate": 115200,
    }
    titanium_lora_pong = {
        "port": "COM6",
        "baudrate": 115200,
    }

    serial_ping = (SerialBuilder.read_configuration()
                                .update_port(titanium_lora_ping.get("port"))
                                .update_baudrate(titanium_lora_ping.get("baudrate"))
                                .build())
    serial_pong = (SerialBuilder.read_configuration()
                                .update_port(titanium_lora_pong.get("port"))
                                .update_baudrate(titanium_lora_pong.get("baudrate"))
                                .build())
    
    serial_ping.open_serial_port()
    serial_ping.flush()
    serial_pong.open_serial_port()
    serial_pong.flush()
    
    # data_command = b"PING"
    data_command = b" THIS MESSAGE WAS SENT USING LORAWAN PROTOCOL!"

    message = (MessageBuilder.set_memory_area(MessageAreas.LORA_WRITE)
                        .set_command(MessageCommands.WRITE)
                        .set_data(data_command)
                        .build())
    serial_ping.send_byte_stream(message.byte_stream)
    time.sleep(2)
    message = (MessageBuilder.set_memory_area(MessageAreas.LORA_WRITE)
                             .set_command(MessageCommands.READ)
                             .set_data(data_command)
                             .build())
    serial_ping.send_byte_stream(message.byte_stream)
    time.sleep(1)
    print(serial_ping.read_byte_stream())
    time.sleep(1)
    message = (MessageBuilder.set_memory_area(MessageAreas.LORA_READ)
                             .set_command(MessageCommands.READ)
                             .set_data(data_command)
                             .build())
    time.sleep(2)
    serial_pong.send_byte_stream(message.byte_stream)
    time.sleep(1)
    print(serial_pong.read_byte_stream())

lora_test()