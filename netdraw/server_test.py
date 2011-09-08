#!/usr/bin/python

__author__ = "Nick Pascucci (npascut1@gmail.com)"

"""Unit tests for the network drawing server."""

import socket
import subprocess
import time
import unittest
import MobileComputing.netdraw.server as server
from MobileComputing.netdraw.display_test import MockDisplay

SIZE = (640, 480)

class ServerUnitTest(unittest.TestCase):
    """Class for testing individual units of the server."""
    def setUp(self):
        self.mock_display = MockDisplay(SIZE)
        self.server = server.DrawServer(self.mock_display)

    def tearDown(self):
        del self.server

    def testRaisesErrorForSmallPacket(self):
        """Server should raise a parse error for packets that are too short."""
        self.assertRaises(
            server.ParseError,
            self.server._parse_packet,
            "foo")

    def testDrawPoint(self):
        """Server should send commands to the display on receiving packet."""
        packet = "point 0 0 50 50 0 0 255"
        expected_args = ((0,0), (0, 0, 255))
        self.server._parse_packet(packet)
        generated_args = self.mock_display.wasCalled(self.mock_display.drawPoint)
        assert generated_args == expected_args

    def testDrawLine(self):
        """Server should send commands to the display on receiving packet."""
        packet = "line 0 0 50 50 0 0 255"
        expected_args = ((0,0), (50, 50), (0, 0, 255))
        self.server._parse_packet(packet)
        generated_args = self.mock_display.wasCalled(self.mock_display.drawLine)
        assert generated_args == expected_args

    def testDrawRect(self):
        """Server should send commands to the display on receiving packet."""
        packet = "rect 0 0 50 50 0 0 255"
        expected_args = ((0,0), (50, 50), (0, 0, 255))
        self.server._parse_packet(packet)
        generated_args = self.mock_display.wasCalled(self.mock_display.drawRect)
        assert generated_args == expected_args

    def testDrawEllipse(self):
        """Server should send commands to the display on receiving packet."""
        packet = "ellipse 0 0 50 50 0 0 255"
        expected_args = ((0,0), (50, 50), (0, 0, 255))
        self.server._parse_packet(packet)
        generated_args = self.mock_display.wasCalled(
            self.mock_display.drawEllipse)
        assert generated_args == expected_args

    def testDrawRectFilled(self):
        """Server should send commands to the display on receiving packet."""
        packet = "rectf 0 0 50 50 0 0 255"
        expected_args = ((0,0), (50, 50), (0, 0, 255))
        self.server._parse_packet(packet)
        generated_args = self.mock_display.wasCalled(self.mock_display.fillRect)
        assert generated_args == expected_args

    def testDrawEllipseFilled(self):
        """Server should send commands to the display on receiving packet."""
        packet = "ellipsef 0 0 50 50 0 0 255"
        expected_args = ((0,0), (50, 50), (0, 0, 255))
        self.server._parse_packet(packet)
        generated_args = self.mock_display.wasCalled(
            self.mock_display.fillEllipse)
        assert generated_args == expected_args

class ServerIntegrationTest(unittest.TestCase):
    """Class for testing whole-server functionality."""
    def setUp(self):
        self.server = subprocess.Popen(["./server.py", "8090"])
        time.sleep(1) # Wait for server to start
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server.get_ip_addr(), 8090))

    def tearDown(self):
        self.server.kill()

    def testConnection(self):
        """Server should reply with the size of its window when connected to."""
        data = self.socket.recv(4096)
        self.assertTrue(data == "size %d %d" % SIZE)

if __name__ == "__main__":
    unittest.main()
