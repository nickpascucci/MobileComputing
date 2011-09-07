#!/usr/bin/python

__author__ = "Nick Pascucci (npascut1@gmail.com)"

"""Display object for the server."""

import pygame.display
import pygame.draw

class Display:

    BACKGROUND = (255, 255, 255)
    LINE_WIDTH = 5

    def __init__(self, size):
        """Initialize the display.

        Args:
            size: A tuple of (width, height) describing the dimensions.
        """
        self.size = size
        self._display = pygame.display.set_mode(size)
        self._display.fill(self.BACKGROUND)
        pygame.display.set_caption("Netdraw Server")
        pygame.display.flip()

    def drawPoint(self, point, color):
        """Draw a point on the screen.
        """
        pygame.draw.line(
            self._display,
            color,
            point,
            point)
        pygame.display.flip()

    def drawLine(self, point1, point2, color):
        """Draw a line on the screen.
        """
        pygame.draw.line(
            self._display,
            color,
            point1,
            point2,
            self.LINE_WIDTH)
        pygame.display.flip()

    def drawRect(self, point1, point2, color):
        """Draw a rectangle outline on the screen.
        """
        self._doDrawRect(point1, point2, color, False)

    def fillRect(self, point1, point2, color):
        """Draw a filled rectangle on the screen.
        """
        self._doDrawRect(point1, point2, color, True)

    def _doDrawRect(self, point1, point2, color, filled):
        rect = _getRect(point1, point2)
        width = self.LINE_WIDTH
        if filled:
            width = 0
        pygame.draw.rect(
            self._display,
            color,
            rect,
            width)
        pygame.display.flip()


    def drawEllipse(self, point1, point2, color):
        """Draw an ellipse outline on the screen.
        """
        self._doDrawEllipse(point1, point2, color, False)

    def fillEllipse(self, point1, point2, color):
        """Draw a filled ellipse on the screen.
        """
        self._doDrawEllipse(point1, point2, color, True)

    def _doDrawEllipse(self, point1, point2, color, filled):
        rect = _getRect(point1, point2)
        width = self.LINE_WIDTH
        if filled:
            width = 0
        pygame.draw.ellipse(
            self._display,
            color,
            rect,
            width)
        pygame.display.flip()

    def close(self):
        """Close the display."""
        pygame.display.quit()

def _getRect(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    width = x2 - x1
    height = y2 - y1
    rect = pygame.rect.Rect(point1, (width, height))
    return rect
