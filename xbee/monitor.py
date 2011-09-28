#!/usr/bin/python
# Monitor.py - A script to monitor XBee radios.

import serial
import socket
import sys
import threading
import Queue
from MobileComputing.xbee.serialthread import SerialThread
from MobileComputing.xbee.clientthread import ClientThread
from MobileComputing.netdraw.server import get_ip_addr

PORT = 9002

class ServerThread(threading.Thread):
    """Implements a threaded server.

    This class contains a server socket which accepts new connections and
    offloads them to a client handling thread. It also instantiates a new serial
    port thread, which communicates asynchronously with the client handling
    thread to distribute new data.
    """
    def __init__(self, port_name):
        threading.Thread.__init__(self)
        self.input_queue = Queue.Queue()
        self.client_queue = Queue.Queue()
        self.port_name = port_name

    def handle_incoming_connections(self, server_socket):
        server_socket.listen(3)
        while True:
            client_socket, address = server_socket.accept()
            print "Accepted new client", address
            self.client_queue.put(client_socket) # This may block if queue full.

    def connect_serial(self):
        print "Attempting to connect to", self.port_name
        try:
            return serial.Serial(self.port_name) # Defaults are ok: 9600 8N1
        except:
            return None
            
    def run(self):
        serport = self.connect_serial()
        if not serport:
            print "Could not connect to serial port."
            sys.exit(1)
        else:
            print "Success!"

        serial_thread = SerialThread(serport, self.input_queue)
        serial_thread.daemon = True
        serial_thread.start()

        # This queue stores sockets produced by the server. They are consumed
        # by the client thread, stored, and used to send data.
        client_thread = ClientThread(self.client_queue,
                                     self.input_queue)
        client_thread.daemon = True
        client_thread.start()

        # The "with" keyword here automatically closes the socket for us.
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = get_ip_addr() # Imported from MobileComputing.netdraw.server
        server_socket.bind((addr, PORT))
        print "Bound to", addr
        self.handle_incoming_connections(server_socket)
        server_socket.close()

if __name__ == "__main__":
    port = 0
    if len(sys.argv) > 1:
        port = sys.argv[1]
    server = ServerThread(port)
    server.daemon = True
    print "Press Enter to quit."
    server.start()
    raw_input("")
