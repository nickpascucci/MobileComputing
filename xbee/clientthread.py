# clientthread.py - Threading for socket based clients.

import threading
import socket
import Queue

class ClientThread(threading.Thread):
    """Implements a threaded consumer object which can handle multiple clients.

    This object maintains a listing of network sockets and receives data from
    a synchronized queue. After being notified by an input event, the object
    dequeues new data, formats it, and sends it out to registered sockets."""

    def __init__(self, client_queue, input_queue):
        threading.Thread.__init__(self)
        self.client_queue = client_queue
        self.input_queue = input_queue
        # We'll store clients we receive from the queue here.
        self.clients = []

    def run(self):
        while True:
            # Add any new clients to the queue.
            self.handle_new_clients()
            self.handle_new_data()

    def handle_new_clients(self):
        """Get a new client socket from the client queue and begin servicing it.
        """
        while not self.client_queue.empty():
            try:
                # We'll attempt to pull our new client out of the queue, but
                # only if we can do so without blocking.
                self.clients.append(self.client_queue.get(False))
            except Queue.Empty:
                pass

    def handle_new_data(self):
        """Read, format, and distribute new data."""
        # We'll try to read all of the available data at once.
        while not self.input_queue.empty():
            try:
                # We're the only consumer thread, so we can safely remove data.
                data = self.input_queue.get(False)
                data = self.format_data(data)
                # Note: We're making a copy of self.clients here. This is so
                # we can safely mutate self.clients without skipping elements.
                for client in self.clients[:]:
                    try:
                        client.send(data)
                    except socket.error, e:
                        # Broken pipe, client has disconnected. Remove them
                        # from our list and carry on.
                        self.clients.remove(client)
                        print "Client disconnected. %d remaining." % (
                            len(self.clients))

            except Queue.Empty:
                # The data should have been in the queue, but if it isn't
                # it's no big deal - we haven't modified any object state.
                break

    def format_data(self, data):
        """Format the data to match application level protocol."""
        # For now, just a stand in.
        return data
