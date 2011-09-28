# xbee_formatter.py - A formatter for XBee Series 2 packets.

import struct

def format(packet):
    # The frame consists of:
    # 0: 0x7E to start the frame
    # 1 & 2: Length.
    # 3 -> length-1: Data
    # last: Checksum.
    # When we pull out the data, wee get a packet that has 13 bytes of metadata:
    # 0: API ID. This is generally 0x10, a ZigBee Tx Request.
    # 1: Frame ID.
    # 2-9: 64 bit address.
    # 10 & 11: 16 bit address.
    # 12: Broadcast radius.
    # 13: Option. Generally ZB_TX_UNICAST.
    # 14+: Data.
    tx_address = packet[10:12]
    # For now, we'll assume the data portion contains 10 uint16_t shorts.
    frame_data = packet[15:-1]  

    formatted_packet = bytearray()
    for i in range(4):
        formatted_packet.append("\0")  # Pad with null bytes.
    # Last byte of tx_address is what we'll use for source id's.
    formatted_packet.append(tx_address[1] & 0xff)
    for i in range(11):
        formatted_packet.append("\0")
    formatted_packet.extend(frame_data)
    return formatted_packet

    

