#!/usr/bin/python
# Interface to the Wiimote over Bluetooth.

import bluetooth

ACCEL_MODE = 0x52120031
BUTTON_MODE = 0x52120030

# Data Constants
BUTTON_PRESSED = 0
BUTTON_RELEASED = 1

# Convert a number into a list of bytes
def to_byte_list(val):
	result = []
	while val:
		tmp = val & 0xff
		result.append(tmp)
		val = val >> 8
	result.reverse()
	return result

class WiiMote(Object):
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
        self.set_mode(BUTTON_MODE)

    def set_mode(self, mode):
        """Set the wiimote mode."""
        self.mode = mode
        self.send_data(to_byte_list(mode))

    def _interpret_packet(self, packet):
        """Read a packet and call the listener functions."""

    def _send_button_event(self, data):
        """Send an event to button listeners.

        Args:
          data: An 11-tuple representing the button states.
        """
        pass

    def _send_accelerometer_event(self, data):
        """Send an event to the accelerometer listeners.

        Args:
          data: A 3-tuple representing accelerometer values.
        """
        pass

    # Send a list of bytes out
    def send_data(self, data):
        str_data = ""
        for each in data:
            str_data += chr(each)
            self.osocket.send(str_data)

    def run(self):
        """Enter a loop to poll the wiimote and call callback functions."""
        pass


