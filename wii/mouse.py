# Adapted from code at http://ubuntuforums.org/showthread.php?p=5365202

from ctypes import cdll

dll = cdll.LoadLibrary('libX11.so')

class Mouse(object):
    def __init__(self):
        self.location = (50, 50)

    def move_offset(self, x, y):
        self.move_absolute(self.location[0] + x, self.location[1] + y)

    def move_absolute(self, x, y):
        new_location = (x, y)
        d = dll.XOpenDisplay(None)
        root = dll.XDefaultRootWindow(d)
        dll.XWarpPointer(d, None, root, 0, 0, 0, 0,
            new_location[0], new_location[1])
        self.location = new_location
        dll.XCloseDisplay(d)
