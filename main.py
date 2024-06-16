import argparse
import time

from src import SerialBuilder
from src import MessageBuilder
from src import MessageCommands, MessageAreas

def handle_argparse():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Script used to run tests in a QEMU emulated environment"
    )

    parser.add_argument(
        "--baudrate",
        "-b",
        type=int,  # Baudrate is typically an integer
        help="Serial Baudrate. Default is 115200.",
        default=115200,
    )

    parser.add_argument(
        "--port",
        "-p",
        type=str,
        help="Communication port. Default is 'COM3'.",
        default="/dev/tty3",
    )

    parser.add_argument(
        "--file",
        "-f",
        type=str,
        help="Path to a file containing the command to send.",
    )

    parser.add_argument(
        "--payload",
        type=str,
        help="Payload to send directly as a command.",
    )

    parser.add_argument(
        "--command",
        "-c",
        type=str,
        choices=["R", "W", "r", "w"],
        help="Command to interact with the requested memory area (R for read, W for write).",
    )

    parser.add_argument(
        "--memory_area",
        "-m",
        type=int,
        help="Firmware memory area to access through serial.",
    )
    
    parser.add_argument(
        "--timeout",
        "-t",
        type=int,
        help="Timeout in seconds for waiting for a response from the host. Default is 20 seconds.",
        default=5,
    )

    args = parser.parse_args()

    if args.file and args.payload:
        parser.error(
            "Arguments --file and --payload are mutually exclusive. Provide only one."
        )
    elif not args.file and not args.payload:
        parser.error("One of --file or --payload must be provided.")

    return args


def main():
    args = handle_argparse()
    payload = None

    serial = (
        SerialBuilder.read_configuration()
        .update_port(args.port)
        .update_baudrate(args.baudrate)
        .build()
    )

    serial.open_serial_port()
    serial.flush()

    if args.file:
        with open(args.file, 'rb') as file:
            payload = file.read()
    else:
        payload = args.payload.encode()

    message = (
        MessageBuilder.set_memory_area(args.memory_area)
        .set_command(args.command)
        .set_data(payload)
        .build()
    )
    
    serial.send_byte_stream(message.byte_stream)
    # time.sleep(0.25)  # Adjust sleep time as needed
    

    print("Message sent to the host, waiting for host reply...")
    
    start_time = time.time()
    while (time.time() - start_time) < args.timeout:
        response = serial.read_byte_stream()
        if len(response) > 0:
            print(response)
        if b"NAK" in response or b"ACK" in response:
            break
        time.sleep(0.1)  # Adjust sleep time as needed


if __name__ == "__main__":
    main()
