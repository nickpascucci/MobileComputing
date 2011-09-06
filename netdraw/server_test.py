#!/usr/bin/python
# Unit tests for network drawing server.

__author__ = "Nick Pascucci (npascut1@gmail.com)"

"""Unit tests for the network drawing server."""

import unittest
import MobileComputing.netdraw.server as srv

class ServerTest(unittest.TestCase):
    def setUp(self):
        self.server = srv.DrawServer()

    def tearDown(self):
        del self.server

    def test_connection(self):
        pass

    def test_create_window(self):
        pass

    def test_draw_line(self):
        pass

    def test_draw_rect(self):
        pass

    def test_draw_ellipse(self):
        pass

    def test_draw_point(self):
        pass

if __name__ == "__main__":
    unittest.main()
