#!/usr/bin/python

__author__ = "Nick Pascucci (npascut1@gmail.com)"

"""Display object for the server."""

import pygame.display
import pygame.draw

class Display(object):

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

        Args:
          point: A tuple (x, y) representing the point's 2D coordinates.
          color: A tuple (R, G, B) representing the color. Values between 0-255.
        """
        pygame.draw.line(
            self._display,
            color,
            point,
            point)
        pygame.display.flip()

    def drawLine(self, point1, point2, color):
        """Draw a line on the screen from point1 to point2.

        Args:
          point1: The start point as a tuple (x, y).
          point2: The end point as a tuple (x, y).
          color: A tuple (R, G, B) representing the color. Values between 0-255.
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

        Args:
          point1: The first corner point as a tuple (x, y).
          point2: The second (diagonal) corner point as a tuple (x, y).
          color: A tuple (R, G, B) representing the color. Values between 0-255.
        """
        self._doDrawRect(point1, point2, color, False)

    def fillRect(self, point1, point2, color):
        """Draw a filled rectangle on the screen.

        Args:
          point1: The first corner point as a tuple (x, y).
          point2: The second (diagonal) corner point as a tuple (x, y).
          color: A tuple (R, G, B) representing the color. Values between 0-255.
        """
        self._doDrawRect(point1, point2, color, True)

    def _doDrawRect(self, point1, point2, color, filled):
        """Perform the actual draw operation.

        Args:
          point1: The first corner point as a tuple (x, y).
          point2: The second (diagonal) corner point as a tuple (x, y).
          color: A tuple (R, G, B) representing the color. Values between 0-255.
          filled: Whether the rectangle should be filled or an outline.
        """
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

        The ellipse is drawn in a bounding box with diagonally opposite corners
        given by point1 and point2.

        Args:
          point1: The first corner point as a tuple (x, y).
          point2: The second (diagonal) corner point as a tuple (x, y).
          color: A tuple (R, G, B) representing the color. Values between 0-255.
        """
        self._doDrawEllipse(point1, point2, color, False)

    def fillEllipse(self, point1, point2, color):
        """Draw a filled ellipse on the screen.

        The ellipse is drawn in a bounding box with diagonally opposite corners
        given by point1 and point2.

        Args:
          point1: The first corner point as a tuple (x, y).
          point2: The second (diagonal) corner point as a tuple (x, y).
          color: A tuple (R, G, B) representing the color. Values between 0-255.
        """
        self._doDrawEllipse(point1, point2, color, True)

    def _doDrawEllipse(self, point1, point2, color, filled):
        """Perform the actual draw operation.

        Args:
          point1: The first corner point as a tuple (x, y).
          point2: The second (diagonal) corner point as a tuple (x, y).
          color: A tuple (R, G, B) representing the color. Values between 0-255.
          filled: Whether the ellipse should be filled or an outline.
        """
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
    """Get a pygame.rect.Rect object from two diagonal corners.

    Args:
      point1: The first corner point as a tuple (x, y).
      point2: The second (diagonal) corner point as a tuple (x, y).

    Returns:
      A pygame.rect.Rect with diagonally opposing corners at point1 and point2.
    """
    x1, y1 = point1
    x2, y2 = point2
    width = x2 - x1
    height = y2 - y1
    rect = pygame.rect.Rect(point1, (width, height))
    return rect
