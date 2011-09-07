import hashlib
import random

def packetize(msg, port):
    packets = []
    seq_num = 0
    for i in range(0, len(msg), 49):
        data = msg[i:i+49]
        packets.append(make_packet(data, port, seq_num))
        seq_num += 1
    return packets


def make_packet(data, port, sequence):
    sequence = str(sequence)
    sequence = (5 - len(sequence)) * "0" + sequence
    port = str(port)
    port = (5 - len(port)) * "0" + port
    data += (49 - len(data)) * "0"
    checksum = hashlib.md5(data).hexdigest()[:5]
    packet = "%s%s%s%s" % (port, sequence, checksum, data)
    return packet

def textify(packets):
    random.shuffle(packets)
    textfile = open("packets.txt", "w")
    for packet in packets:
        textfile.write(packet)
        textfile.write("\n")

