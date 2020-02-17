import serial
import struct
import threading

# Serial implements the framing protocol of the portable70
# serial port.
# The 0x7D byte is used as escape sequence for the following byte
# where the bytes [0x01, 0x02, 0x7D] are reserved.
# 0x01: Start of frame
# 0x02: End of frame
# 0x7D: 0x7D escaped
class Serial:
    ser = None
    escaped = False
    started = False
    lbuf = []
    cb = None

    def __init__(self, port, baud, cb):
        # open the serial port
        self.ser = serial.Serial(port, baud)
        self.cb = cb

    def send(self, buf):
        frm = [0x7D, 0x01]
        for i in buf:
            if i == 0x7D:
                frm.append(0x7D)

            frm.append(i)

        frm.append(0x7D)
        frm.append(0x02)
        print(frm)
        self.ser.write(frm)

    def append(self, b):
        # append the byte to the buffer
        self.lbuf.append(b)

    def handle(self):
        self.cb(self.lbuf)

    def thread(self):
        # read the incoming data from the serial port
        while True:

            # read the available bytes from the serial port
            buf = bytearray(self.ser.read())
            if len(buf) == 0:
                continue

            # get the first byte
            b = buf[0]

            if self.escaped and b == 0x7D:
                self.escaped = False
                self.append(b)
                continue

            # if this byte is currently not escaped, and the escape
            # code is sent, mark the next byte as escaped
            if (not self.escaped) and b == 0x7D:
                self.escaped = True
                continue

            # if the byte is escaped and the start code was received
            if self.escaped and b == 0x01:
                self.started = True
                self.escaped = False
                self.fbuf = []
                self.lbuf = []
                continue

            # if the byte is escaped and the stop code was received
            if self.escaped and b == 0x02:
                self.started = False
                self.escaped = False

                self.handle()
                continue

            # if this is just a regular byte, append it to the buffer
            if self.started:
                self.append(b)
                continue

    def start(self):
        threading.Thread(target=self.thread).start()
