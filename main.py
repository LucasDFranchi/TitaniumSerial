from time import sleep

from src import SerialBuilder
from src import MessageBuilder
from src import MessageCommands, MessageAreas

def main():
    serial = SerialBuilder.build()
    message = (MessageBuilder.set_memory_area(MessageAreas.DISPLAY)
                             .set_command(MessageCommands.WRITE)
                             .set_data(bytearray([255] * 1))
                             .build())

    serial.open_serial_port()
    error_counter = 0
    for _ in range(1000*1024):
        serial.send_byte_stream(message.byte_stream)
        sleep(0.25)
        if serial.read_byte_stream() != b'ACKOK00':
            error_counter += 1

    print(f"A error occur in {error_counter}% of transmissions")


if __name__ == "__main__":
    main()