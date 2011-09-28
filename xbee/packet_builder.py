# packet_builder.py - A byte-by-byte packet builder for XBee Series 2 radios.

import struct

START_BYTE = 0x7e

class PacketBuilder(object):
    def __init__(self):
        self.bytes = bytearray()
        self.length = -1
        self.packet = None
        self.packet_complete = False

    def add_byte(self, raw_byte):
        byte, = struct.unpack("B", raw_byte)
        if len(self.bytes) == 0 and byte != START_BYTE:
            return
        elif byte == START_BYTE:
            # Start over!
            self.bytes = bytearray()
            self.bytes.append(byte)
            self.packet = None
            self.length = -1
            self.packet_complete = False
        else:
            self.bytes.append(byte)
            self.attempt_parse()

    def attempt_parse(self):
        if len(self.bytes) == 3:
            # We can now unpack the two length bytes.
            self.length, = struct.unpack(">H", str(self.bytes[1:]))

        elif (self.length > 0 and
              len(self.bytes) == self.length + 5):
            # Complete packet. Parse it, send it.
            self.packet = self.parse_frame()

            if self.packet:
                self.packet_complete = True

            # Reset.
            self.bytes = bytearray()
            self.length = -1

    def parse_frame(self):
        """Parse a complete packet by escaping it and verifying the checksum.
        """
        # Format: START_BYTE, LengthMSB, LengthLSB, APIID, DATA, ... , CHECKSUM
        # Length short only contains length of data field.

        # Unpack returns a tuple, even when there's only one value. Hence the comma.
        # We want a big endian, unsigned short from the 2nd and 3rd bytes.
        packet = self.bytes[:]
        packet = self.escape(packet)
        if self.verify(packet):
            return packet
        else:
            return None

    def verify(self, packet):
        """Verify the packet against its checksum.

        The checksum is calculated by calculating the sum of the data bytes modulo
        0xff, and subtracting that result from 0xff. To verify the packet, we sum
        all of the bytes (including the checksum), and check that it is equal to
        0xff.

        """
        if not packet:
            return False

        data_bytes = packet[3:]
        data_sum = sum(data_bytes)
        result = data_sum & 0xff
        if result == 0xff:
            return True
        return False

    def escape(self, packet):
        """Scan the packet and escape appropriate bytes."""
        escaped_data = bytearray()
        escape = False
        for byte in packet:
            if byte == 0x7D:
                # Escape byte. We'll escape the next one.
                escape = True
            elif escape:
                # That would be this one.
                val = byte ^ 0x20
                escaped_data.append(val)
                escape = False
            else:
                escaped_data.append(byte)
        return escaped_data
