#!/usr/bin/python
# Server for network drawing program.

__author__ = "Nick Pascucci (npascut1@gmail.com)"

import socket
import logging

PORT = 6060

class DrawServer:
    """Server waits for incoming connections and creates a window to draw on."""

    def __init__(self):
        logging.debug("Creating socket.")
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        logging.info("Accepting new connections on port %d." % PORT)
        while True:
            conn, address = self._socket.accept()
            logging.debug("Accepted new connection from %s." % address)

