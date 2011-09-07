#!/usr/bin/python

__author__ = "Nick Pascucci (npascut1@gmail.com)"

"""Unit tests for the display."""

import unittest
import MobileComputing.netdraw.display as display
import pygame.display

COLOR = (50, 50, 50)
SIZE = (640, 480)

class DisplayTest(unittest.TestCase):
    def setUp(self):
        self.display = display.Display(SIZE)

    def tearDown(self):
        del self.display

    def testClose(self):
        """The display should close all windows when done."""
        self.display.close()
        assert pygame.display.get_surface() == None

    def testGetSize(self):
        """The display should return a tuple of its size."""
        assert self.display.size == SIZE

    def testDrawPoint(self):
        """drawPoint should draw a point on the screen."""
        self.display.drawPoint((320, 240), COLOR)

    def testDrawLine(self):
        """drawLine should draw a line on the screen."""
        self.display.drawLine((300, 200), (340, 280), COLOR)

    def testDrawRect(self):
        """drawRect should draw a rectangle on the screen."""
        self.display.drawRect((300, 200), (340, 280), COLOR)
        self.display.fillRect((300, 200), (340, 280), COLOR)

    def testDrawEllipse(self):
        """drawEllipse should draw an ellipse on the screen."""
        self.display.drawEllipse((300, 200), (340, 280), COLOR)
        self.display.fillEllipse((300, 200), (340, 280), COLOR)


class WasNotCalledError(Exception):
    """Generic exception for testing."""
    pass

class MockDisplay():
    def __init__(self, size):
        self.size = size
        self.called_functions = {}

    def wasCalled(self, function):
        if function in self.called_functions:
            return self.called_functions[function]
        else:
            raise WasNotCalledError("Function %s was not called." % function)

    def drawPoint(self, point, color):
        self.called_functions[self.drawPoint] = (point, color)

    def drawLine(self, point1, point2, color):
        self.called_functions[self.drawLine] = (point1, point2, color)

    def drawRect(self, point1, point2, color):
        self.called_functions[self.drawRect] = (point1, point2, color)

    def fillRect(self, point1, point2, color):
        self.called_functions[self.fillRect] = (point1, point2, color)

    def drawEllipse(self, point1, point2, color):
        self.called_functions[self.drawEllipse] = (point1, point2, color)

    def fillEllipse(self, point1, point2, color):
        self.called_functions[self.fillEllipse] = (point1, point2, color)

    def close(self):
        self.called_functions[self.close] = ()

if __name__ == "__main__":
    unittest.main()
