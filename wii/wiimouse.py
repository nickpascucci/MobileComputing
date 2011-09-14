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
def click_mouse(data): # Callback for mouse clicks
    global left_down
    global right_down
    if data["a"]:
        args = ["xdotool", "mousedown", "1"]
        subprocess.Popen(args)
        left_down = True
    elif left_down:
        args = ["xdotool", "mouseup", "1"]
        subprocess.Popen(args)
        left_down = False

    if data["minus"]:
        args = ["xdotool", "mousedown", "3"]
        subprocess.Popen(args)
        right_down = True
    elif right_down:
        args = ["xdotool", "mouseup", "3"]
        subprocess.Popen(args)
        right_down = False

wm.register_ir_listener(move_mouse)
wm.register_button_listener(click_mouse)
wm.run()
