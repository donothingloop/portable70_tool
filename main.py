import argparse

import matplotlib.pyplot as plt
import matplotlib
import time
import struct
import threading
import rssi

from api import API
from pserial import Serial
from scipy import signal

# default usb serial port
device = '/dev/ttyUSB0'
baud = 1000000
config = False

# parse the commandline arguments
parser = argparse.ArgumentParser(
    description='FFT tool for the portable70 spectrum analyzer firmware.')
parser.add_argument('--device', type=str, dest='device',
                    action='store', default=device)
parser.add_argument('--baud', type=int, dest='baud',
                    action='store', default=baud)
parser.add_argument('--config', dest='config', help='Update the devices config',
                    action='store_true')
parser.add_argument('--persist', dest='persist', help='Save the config to the flash',
                    action='store_true')
parser.add_argument('--freq', dest='freq', help='Config: Set the frequency (Hz)',
                    action='store')
parser.add_argument('--offset', dest='offset', help='Config: Set the tx offset (Hz)',
                    action='store')
parser.add_argument('--callsign', dest='callsign', help='Config: Set the callsign (max. 8 chars)',
                    action='store')
parser.add_argument('--rssi', dest='rssiDump',
                    help='Config: enable rssi dump', action='store_true')
args = parser.parse_args()

api = API()

ser = Serial(args.device, args.baud, api.handle)
ser.start()

vrssi = rssi.RSSI(api)

if args.config:
    print("Updating config.")
    buf = api.config({
        "persist": args.persist,
        "freq": args.freq,
        "offset": args.offset,
        "callsign": args.callsign,
        "rssiDump": args.rssiDump,
    })
    ser.send(buf)


def printLog(msg):
    print(msg.log.message)

# listen for log messages from the firmware
api.receive('log', printLog)

if args.rssiDump:
    vrssi.start()

    while True:
        time.sleep(0.01)
        vrssi.plot()
