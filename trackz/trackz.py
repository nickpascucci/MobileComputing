#! /usr/bin/python

"""Trackz desktop client.

Interfaces to the Android client over Bluetooth."""

import bluetooth
import logging
import uuid

PORT = 1002
UUID = "2f5ffe67-81f1-4e9b-8636-370b83607639"

def listen(client_sock):
    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            else:
                parse(data)
    except IOError:
        logging.error("IOError occurred.")
        return

def parse(data):
    print data

def main():
    # Open a socket and bind to a known address
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(10)
    print "Listening on channel", server_sock.getsockname()
    bluetooth.advertise_service(server_sock,
                                "Trackz Service",
                                service_id = UUID,
                                service_classes = [UUID,
                                                   bluetooth.SERIAL_PORT_CLASS],
                                profiles = [bluetooth.SERIAL_PORT_PROFILE]
                                )
    print "Advertising service."
    # Accept new connections
    print "Waiting on new connections."
    client_sock, client_info = server_sock.accept()
    print "Accepted connection from", client_info

    # When the first connection is established, verify its identity
    try:
        client_sock.send("TRACKZ")
        print "Sent TRACKZ."
        data = client_sock.recv(1024)
        if data == "TRACKZ":
            # Now accept new input events and send them to the mouse.
            print "Great, got the right reply!"
            listen(client_sock)
        else:
            print "Got incorrect reply."
    except:
        pass

    client_sock.close()
    server_sock.close()
    logging.info("Goodbye!")

if __name__ == "__main__":
    main()
