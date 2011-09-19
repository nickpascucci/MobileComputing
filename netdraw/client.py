#!/usr/bin/python
# Client for network drawing program.

import re
import socket
import sys

class Client(object):
    """Batch and interactive client for netdraw server."""
    def __init__(self, socket, srv_size):
        """Initialize a new client with the provided socket.

        Args:
          socket: A socket to the server.
          srv_size: The size of the server screen as a tuple.
        """
        self._socket = socket
        self._size = srv_size

    def sendFile(self, file):
        """Read commands from a file and send them to the server.

        Args:
          file: A text file.
        """
        valid_lines = [line for line in file if validate(line)]
        self.sendToServer(valid_lines)
        
    def sendToServer(self, commands):
        """Send a list of commands to the server.

        Args:
          commands: A list of commands, in string form.
        """
        for string in commands:
            print "Sending %s." % string
            self._socket.sendall(string)

def validate(string):
    """Validate the string to see if it matches the protocol."""
    # I can't believe this worked the first time, but it passes the tests!
    is_valid = bool(re.match(("\\A(point|line|rect|rectf|ellipse|ellipsef) "
                          # Matching any integer for coordinates.
                          "[0-9]+ "
                          "[0-9]+ "
                          "[0-9]+ "
                          "[0-9]+ "
                          # Matching 0-255 for colors.
                          "([0-9]|0[0-9]|00[0-9]"
                          "|[0-9][0-9]|0[0-9][0-9]"
                          "|1[0-9][0-9]"
                          "|2[0-4][0-9]|25[0-5]) "
                          # Again
                          "([0-9]|0[0-9]|00[0-9]"
                          "|[0-9][0-9]|0[0-9][0-9]"
                          "|1[0-9][0-9]"
                          "|2[0-4][0-9]|25[0-5]) "
                          # Again.
                          "([0-9]|0[0-9]|00[0-9]"
                          "|[0-9][0-9]|0[0-9][0-9]"
                          "|1[0-9][0-9]"
                          "|2[0-4][0-9]|25[0-5])\n?"
                          "\\Z"), string))
    print string, "is valid:", is_valid
    return is_valid

def print_help():
    print """client.py: A batch/interactive client for netdraw servers.

    Usage:
    client.py -i <server:port>         Interactive mode
    client.py -b <file> <server:port>  Batch mode
    client.py -h                       Print this help message
    """

def parse_addr(addr):
    """Parse a string into a (server, port) tuple."""
    addr = addr.split(":")
    server = addr[0]
    port = int(addr[1])
    return (server, port)

if __name__ == "__main__":
    addr = parse_addr(sys.argv[-1])
    filename = ""
    interactive_mode = False
    for pos, arg in enumerate(sys.argv[1:-1], 1):
        if arg == "-i":
            interactive_mode = True
            break
        elif arg == "-b":
            filename = sys.argv[pos+1]
            break
        elif arg == "-h":
            print_help()
            sys.exit(0)
        else:
            print "Uknown argument %s." % arg
            print_help()
            sys.exit(1)
    print "Connecting to %s on port %d." % addr
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(addr)
    except:
        print "Sorry, could not connect to %s:%d." % addr
        sys.exit(1)

    srv_size = tuple(sock.recv(4096).split(" ")[:2])
    client = Client(sock, srv_size)
    if interactive_mode:
        print "Entering interactive mode."
        print "Enter Ctrl+D (EOF) to exit."
        while True:
            try:
                cmd = raw_input("--> ")
                if validate(cmd):
                    client.sendToServer([cmd])
                else:
                    print "Invalid command %s." % cmd
            except EOFError:
                print "Goodbye!"
                sys.exit(0)
    elif filename:
        print "Reading commands from", filename
        cmd_file = open(filename, "r")
        client.sendFile(cmd_file)
        raw_input("Done! Press enter to exit.")
