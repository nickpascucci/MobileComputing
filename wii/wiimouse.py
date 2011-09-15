#! /usr/bin/python

import wiimote
import mouse
import subprocess

wm = wiimote.WiiMote()
m = mouse.Mouse()

x_size = 1280.0
y_size = 800.0

def move_mouse(data): # Callback for ir tracking
    x = x_size - (data["ir_x"] * (x_size / 1024))
    y = data["ir_y"] * (y_size / 768)
    m.move_absolute(int(x), int(y))

left_down = False
right_down = False

wm.register_ir_listener(move_mouse)
wm.register_button_listener(click_mouse)
wm.run()
