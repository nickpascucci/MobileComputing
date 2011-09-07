#!/usr/bin/python
# Server for network drawing program.

__author__ = "Nick Pascucci (npascut1@gmail.com)"

import logging
import signal
import socket
import threading
from MobileComputing.netdraw import display

logging.basicConfig(level=logging.DEBUG)

PORT = 6060

# Server is started, so it creates a socket to listen on and spawns a listener
# to detach from the main process.

class ParseError(Exception):
    """Generic parsing error."""
    pass

class DrawServer:
    """Server waits for incoming connections and creates a window to draw on."""

    def __init__(self, display):
        self.display = display

    def start(self):
        """Start the server and accept incoming connections."""
        logging.debug("Creating socket.")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = self._get_ip_addr() # socket.gethostbyname(socket.gethostname())
        self.socket.bind((addr, PORT))
        logging.debug("Bound to %s:%d" % (addr, PORT))
        sockname = self.socket.getsockname()
        logging.info("Accepting new connections on %s port %d." % sockname)
        self.socket.listen(0)
        while True:
            conn, address = self.socket.accept()
            logging.debug("Accepted new connection from %s." % address)

    def stop(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def _parse_packet(self, packet):
        """Parse a packet to determine its intent."""
        contents = packet.split(" ")
        if len(contents) < 8:
            logging.error("Received incomplete packet.")
            raise ParseError("Packet too short.")
        point1 = (int(contents[1]), int(contents[2]))
        point2 = (int(contents[3]), int(contents[4]))
        color = (int(contents[5]), int(contents[6]), int(contents[7]))
        type = contents[0]
        if type == "point":
            self.display.drawPoint(point1, color)
        elif type == "line":
            self.display.drawLine(point1, point2, color)
        elif type == "rect":
            self.display.drawRect(point1, point2, color)
        elif type == "ellipse":
            self.display.drawEllipse(point1, point2, color)
        elif type == "rectf":
            self.display.fillRect(point1, point2, color)
        elif type == "ellipsef":
            self.display.fillEllipse(point1, point2, color)

    def _get_ip_addr(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        return s.getsockname()[0]

if __name__ == "__main__":
    screen = display.Display((640, 480))
    server = DrawServer(screen)
    def handle_signal(signum, frame):
        server.stop()
#    signal.signal(signal.SIGKILL, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    server.start()
