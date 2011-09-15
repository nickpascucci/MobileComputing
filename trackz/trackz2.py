#! /usr/bin/python

import bitstring
import bluetooth
import sys
from MobileComputing.wii import mouse

UUID = "2f5ffe67-81f1-4e9b-8636-370b83607639"
maus = mouse.Mouse()

def connect(match):
    print "Connecting to %(name)s on %(port)s." % match
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((match["host"], match["port"]))
    print "Done!"
    while True:
        data = sock.recv(1024)
        process(bytearray(data))

def process(data):
    if not len(data) == 12:
        print "Got funky data, size", len(data)
        return
    move_type = bitstring.BitArray(data[:4]).int
    delta_x = bitstring.BitArray(data[4:8]).int
    delta_y = bitstring.BitArray(data[8:]).int
    if move_type == 1:
        print "Move by ", delta_x, delta_y
        maus.move_offset(delta_x, delta_y)
    elif move_type == 2:
        maus.click_mouse(mouse.LEFT_CLICK)

print "Discovering devices!"

service_matches = bluetooth.find_service(uuid=UUID)

if len(service_matches) == 0:
    print "Sorry, couldn't find the TrackZ service."
    sys.exit(0)

for match in service_matches:
    device = match["name"]
    ans = raw_input("Do you want to connect to device %s? [y/n] " % device)
    if ans == "y":
        connect(match)
        break


# devices = bluetooth.bluez.discover_devices(lookup_names=True)
# if len(devices) < 1:
#     print "No devices found. Sorry!"
#     sys.exit(0)
# for address, device in devices:
#
