#!/usr/bin/python
# Interface to the Wiimote over Bluetooth.

import bluetooth

ACCEL_MODE = 0x52120031
BUTTON_MODE = 0x52120030

# Convert a number into a list of bytes
def to_byte_list(val):
    result = []
    while val:
        tmp = val & 0xff
        result.append(tmp)
        val = val >> 8
    result.reverse()
    return result

def print_bytes(string):
    for byte in string:
        print "%x" % int(byte)

def is_on(byte, pos):
    """Check if the given byte is turned on."""
    mask = 0x01 << pos
    return bool(byte & mask)

def _extract_buttons(byte1, byte2):
    """Extract button data from the first two bytes."""
    byte1_buttons = {
        "left": 0,
        "right": 1,
        "down": 2,
        "up": 3,
        "plus": 4
        }
    byte2_buttons = {
        "two": 0,
        "one": 1,
        "b": 2,
        "a": 3,
        "minus": 4,
        "home": 7
        }
    for button, pos in byte1_buttons.iteritems():
        if is_on(byte1, pos):
            byte1_buttons[button] = True
        else:
            byte1_buttons[button] = False
    for button, pos in byte2_buttons.iteritems():
        if is_on(byte2, pos):
            byte2_buttons[button] = True
        else:
            byte2_buttons[button] = False
    byte1_buttons.update(byte2_buttons) # Return the whole map
    return byte1_buttons

def _extract_accel(array):
    x_val = int(array[2]) << 2
    y_val = int(array[3]) << 2
    z_val = int(array[4]) << 2
    if is_on(array[0], 5):
        x_val += 1
    if is_on(array[0], 6):
        x_val += 2
    if is_on(array[1], 5):
        y_val += 2
    if is_on(array[1], 6):
        z_val += 2
    return {"x_accel": x_val, "y_accel": y_val, "z_accel": z_val}

class WiiMote(object):
    """Class encapsulates a wiimote.

    Provides discovery, event management
    """

    def __init__(self):
        # Hardware address for Bluetooth receiver
        bd_addr = "8C:56:C5:3E:DF:73"

        self.isocket = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        self.osocket = bluetooth.BluetoothSocket(bluetooth.L2CAP)

        # 19 and 17 are the magic Wiimote ports
        self.isocket.connect((bd_addr,19))
        self.osocket.connect((bd_addr,17))
        self.button_listeners = []
        self.accel_listeners = []
        self.send_data(to_byte_list(ACCEL_MODE))

    def _interpret_packet(self, packet):
        """Read a packet and call the listener functions.

        Args:
          packet: The bytes of the packet received.
        """
        packet = packet[2:] # Discard the first two bytes.
        bytes = bytearray(packet) # Separate out the bytes
        buttons = _extract_buttons(bytes[0], bytes[1])
        accel = _extract_accel(bytes)
        self._send_button_event(buttons)
        self._send_accelerometer_event(accel)

    def _send_button_event(self, data):
        """Send an event to button listeners.

        Args:
          data: An 11-tuple representing the button states.
        """
        for listener in self.button_listeners:
            listener(data)

    def _send_accelerometer_event(self, data):
        """Send an event to the accelerometer listeners.

        Args:
          data: A 3-tuple representing accelerometer values.
        """
        for listener in self.accel_listeners:
            listener(data)

    def register_accel_listener(self, listener):
        self.accel_listeners.append(listener)

    def register_button_listener(self, listener):
        self.button_listeners.append(listener)

    # Send a list of bytes out
    def send_data(self, data):
        str_data = ""
        for each in data:
            str_data += chr(each)
            self.osocket.send(str_data)

    def run(self):
        """Enter a loop to poll the wiimote and call callback functions.

        This method will block execution until the thread containing it is
        killed.
        """
        while True:
            self.check_for_data()

    def check_for_data(self):
        msg = self.isocket.recv(128)
        print bytearray(msg)
        self._interpret_packet(msg)
