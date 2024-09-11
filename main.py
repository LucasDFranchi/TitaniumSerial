import argparse
import time

from src import SerialBuilder
from src import MessageBuilder
from src import MessageCommands, MessageAreas
from src import Packet

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
        type=int,
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
        "--address",
        "-a",
        type=str,
        help="Address of the device that will receive the message",
    )

    parser.add_argument(
        "--command",
        "-c",
        type=str,
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
    
    parser.add_argument(
        "-l", "--listening",
        action="store_true",
        help="Enable listening mode. In this mode, the program waits for host messages."
    )

    args = parser.parse_args()

    if args.file and args.payload:
        parser.error(
            "Arguments --file and --payload are mutually exclusive. Provide only one."
        )
    elif not args.file and not args.payload:
        parser.error("One of --file or --payload must be provided.")

    return args

def read_payload(args):
    """
    Reads the payload data based on arguments.

    Args:
        args (argparse.Namespace): Parsed arguments object.

    Returns:
        bytes: Payload data read from file or encoded payload string.
    """
    if args.file:
        with open(args.file, 'rb') as file:
            payload = file.read()
    else:
        payload = args.payload.encode()
    return payload

def build_message(args, payload):
    """
    Constructs a message object using provided arguments and payload.

    Args:
        args (argparse.Namespace): Parsed arguments object.
        payload (bytes): Payload data to include in the message.

    Returns:
        Message: Constructed message object.
    """
    message = (
        MessageBuilder.set_memory_area(args.memory_area)
        .set_command(args.command)
        .set_address(args.address)
        .set_data(payload)
        .build()
    )
    return message

def wait_for_response(serial, args):
    """
    Waits for a response from the host after sending a message.

    Args:
        serial: Serial interface object with read_byte_stream method.
        args (argparse.Namespace): Parsed arguments object.
    """    
    start_time = time.time()
    while (time.time() - start_time) < args.timeout:
        response = serial.read_byte_stream()
        if len(response) > 0:
            break
        time.sleep(0.1)
        
    return response


def main():
    args = handle_argparse()

    serial = (
        SerialBuilder.read_configuration()
        .update_port(args.port)
        .update_baudrate(args.baudrate)
        .build()
    )

    serial.open_serial_port()
    serial.flush()
    
    payload = read_payload(args)
    message = build_message(args, payload)
    
    serial.send_byte_stream(message.byte_stream)
    
    if args.command not in [MessageCommands.WRITE_COMMAND]:
        response = wait_for_response(serial, args)
        Packet.from_byte_stream(response)

if __name__ == "__main__":
    main()
