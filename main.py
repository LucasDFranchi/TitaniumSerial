from src import SerialBuilder

def main():
    serial = SerialBuilder.build()

    serial.open_serial_port()

if __name__ == "__main__":
    main()