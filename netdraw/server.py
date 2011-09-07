#!/usr/bin/python

__author__ = "Nick Pascucci (npascut1@gmail.com)"

import logging
import signal
import socket
import sys
import threading
from MobileComputing.netdraw import display

logging.basicConfig(level=logging.DEBUG)

DEFAULT_PORT = 6060

"""Server for the network drawing program.

To use, run this file from the command line. This program takes up to one
optional argument which is interpreted as the port to bind to. The server will
bind to the current internet facing-address, NOT localhost.
"""

class ParseError(Exception):
    """Generic parsing error."""
    pass

class DrawServer(object):
    """Server waits for incoming connections and creates a window to draw on."""

    def __init__(self, display):
        """Create a new draw server.

        Args:
          display: A display object.
        """
        self.display = display

    def start(self, port):
        """Start the server and accept incoming connections.
        
        Args:
          port: The port to listen on.
        """
        logging.debug("Creating socket.")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = _get_ip_addr()
        self.socket.bind((addr, port))
        logging.debug("Bound to %s:%d" % (addr, port))
        
        sockname = self.socket.getsockname()
        logging.info("Accepting new connections on %s port %d." % sockname)
        print "Accepting new connections on %s port %d." % sockname
        self.socket.listen(0)
        
        (conn, address) = self.socket.accept() # conn is a socket.socket object
        self.conn = conn
        logging.debug("Accepted new connection from %s:%d." % address)
        self.conn.send("size %d %d" % self.display.size) # Part of the protocol
        
        while True:
            packet = self.conn.recv(4096)
            if not packet:
                break
            try:
                self._parse_packet(packet)
            except ParseError:
                pass # Occasional empty packet shouldn't kill us.

    def stop(self):
        """Halt the server and release allocated resources."""
        logging.info("Stopping server.")
        if self.conn:
            self.conn.shutdown(socket.SHUT_RDWR)
            self.conn.close()
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        logging.info("Done! Shutting down.")

    def _parse_packet(self, packet):
        """Parse a packet to determine its intent.

        Args:
          packet: A packet string.
        """
        logging.debug("Received packet:\n%s" % packet)
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

def _get_ip_addr():
    """Resolve the network-facing IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    return s.getsockname()[0]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        port = DEFAULT_PORT
    else:
        port = int(sys.argv[1])
    screen = display.Display((640, 480))
    server = DrawServer(screen)

    def handle_signal(signum, frame):
        """Handle a system signal to shut down gracefully."""
        logging.info("Caught SIGTERM.")
        server.stop()
    signal.signal(signal.SIGTERM, handle_signal)

    server.start(port)
