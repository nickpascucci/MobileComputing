#!/usr/bin/python
# Unit tests for network drawing client.

import unittest
from MobileComputing.netdraw import client

#TEST_DATA_FILE = open("client_test_data.txt", "r")
SRV_SIZE = (640, 480)

class ClientTest(unittest.TestCase):
    def setUp(self):
        self.mock_sock = MockSocket()
        self.client = client.Client(self.mock_sock, SRV_SIZE)

    def tearDown(self):
        pass

    def testSendToServer(self):
        """Send to server should send the lines as-is."""
        test_line = "line 0 0 40 40 200 200 200"
        self.client.sendToServer([test_line])
        generated_args = self.mock_sock.wasCalled(self.mock_sock.send)
        assert generated_args[0] == test_line

    def testRejectsInvalidInput(self):
        """Validate should reject improperly formatted inputs."""
        invalid_inputs = [
            "foo", # Too short
            "foo bar baz", # Too short
            "", # Too short
            "a b c d e f g h i j k", # Too many args
            "100 200 300", # Too short
            "10 10 10 10 10 10 10 10", # Right length, bad type
            "line 10 two 30 40 0 0 255", # Right length, bad y1
            "line 300 200 40 0 1 0 600" # Too large in B
            ]
        for arg in invalid_inputs:
            assert not client.validate(arg)

    def testAcceptsValidInput(self):
        """Validate should accept properly formatted inputs."""
        valid_inputs = [
            "point 40 40 80 80 0 0 0",
            "line 40 40 80 80 0 0 0",
            "rect 80 80 40 40 0 255 0",
            "ellipse 80 80 40 40 0 255 0",
            "rectf 80 80 40 40 0 255 0",
            "ellipsef 80 80 40 40 255 255 36",
            ]
        for arg in valid_inputs:
            assert client.validate(arg)

    def testParseAddr(self):
        addr = "127.0.0.1:80"
        parsed = client.parse_addr(addr)
        assert parsed == ("127.0.0.1", 80)
            
class WasNotCalledError(Exception):
    """Generic exception for testing."""
    pass
        
class MockSocket(object):
    def __init__(self):
        self.called_functions = {}

    def wasCalled(self, function):
        if function in self.called_functions:
            return self.called_functions[function]
        else:
            raise WasNotCalledError("Function %s was not called." % function)

    def send(self, string, flags=0):
        self.called_functions[self.send] = (string, flags)

    def recv(self, bufsize, flags=0):
        self.called_functions[self.send] = (bufsize, flags)


    
if __name__ == "__main__":
    unittest.main()
