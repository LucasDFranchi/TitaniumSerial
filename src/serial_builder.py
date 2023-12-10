import configparser
import serial

class SerialBuilder:
    _port = None
    _baudrate = None
    _timeout = None
    _parity = None
    _stop_bits = None
    _byte_size = None

    @classmethod
    def build(cls):
        return cls.ByteSender(cls._port, cls._baudrate, cls._timeout, cls._parity, cls._stop_bits, cls._byte_size)

    @classmethod
    def read_configuration(cls):
        _config = configparser.ConfigParser()
        _config.read('config.ini')

        cls._port      = _config.get('SerialConfig', 'port')
        cls._baudrate  = _config.getint('SerialConfig', 'baudrate')

        cls._timeout   = _config.getfloat('SerialConfig', 'timeout', fallback=1.0)
        cls._parity    = _config.get('SerialConfig', 'parity', fallback='N')
        cls._stop_bits = _config.getint('SerialConfig', 'stop_bits', fallback=1)
        cls._byte_size = _config.getint('SerialConfig', 'byte_size', fallback=8)

        return cls
    
    @classmethod
    def update_port(cls, port: str):
        cls._port = port

        return cls

    @classmethod
    def update_baudrate(cls, baudrate: int):
        cls._baudrate = baudrate

        return cls

    class ByteSender:
        def __init__(self, port, baud_rate, timeout, parity, stop_bits, byte_size):
            self._serial = serial.Serial()
            self._serial.port = port
            self._serial.baudrate = baud_rate
            self._serial.bytesize = byte_size
            self._serial.parity = parity
            self._serial.stopbits = stop_bits
            self._serial.timeout = timeout

        def open_serial_port(self):
            self._serial.open()

        def close_serial_port(self):
            self._serial.close()

        def send_byte_stream(self, byte_stream: bytearray):
            self._serial.write(byte_stream)

        def read_byte_stream(self):
            return self._serial.read_all()

        def flush(self):
            self._serial.reset_input_buffer()
            self._serial.reset_output_buffer()
