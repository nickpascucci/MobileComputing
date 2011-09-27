# serialthread.py - Threading for monitoring serial interfaces.

import serial
import threading
import Queue

class SerialThread(threading.Thread):
    """Simple thread to monitor the serial interface."""
    def __init__(self, serport, data_queue):
        threading.Thread.__init__(self)
        self.serport = serport
        self.data_queue = data_queue

    def __del__(self):
        self.serport.close()
        
    def run(self):
        while True:
            data = self.serport.read()
            self.data_queue.put(data)
