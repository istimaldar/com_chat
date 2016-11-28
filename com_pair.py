import serial
import threading


class PairOfPorts():
    def __init__(self, port, func=(lambda string: print(string))):
        self.WritingPort = serial.Serial(port, timeout=1)
        self.ReadingPort = serial.Serial(port, timeout=1)
        read_thread = threading.Thread(target=self.read, name="reader", args=[func])
        self.need_to_read = True
        read_thread.start()

    def write(self, data):
        message = data.encode("ascii")
        self.WritingPort.write(message)

    def read(self, func=(lambda string: print(string))):
        while self.need_to_read:
            message = b''
            data = self.ReadingPort.read(1)
            while data != b'':
                message += data
                data = self.ReadingPort.read(1)
            if len(message):
                func(message)

    def stop(self):
        self.need_to_read = False