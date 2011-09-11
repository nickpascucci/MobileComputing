# Environment Class
# Fisherman class
# Fish class

import Tkinter
import random


def draw_sprite(sprite, canvas, location):
    id = canvas.create_image(location[0], location[1], image=sprite)

class Fisherman(object):
    STATE_FISHING = 1
    STATE_CASTING = 2
    STATE_RETRACT = 3
    STATE_WAITING = 4

    def __init__(self):
        self.casting_state = STATE_WAITING

    def animate(self, num_millis, canvas):
        """Animate the sprite based on state."""

class Fish(object):
    
    def __init__(self):
        self.location = (0, 0)
        self.sprite = Tkinter.PhotoImage(file = "fish.gif")
        self.velocity = 10

    def animate(self, num_millis, canvas):
        """Move in semi-random directions."""
        
        #needs to have randomized sign
        self.direction = (random.random(),random.random())
        self.location = (self.location[0]+num_millis*self.velocity*self.direction[0], 
            self.location[1] + num_millis*self.velocity*self.direction[1])
        print "Drawing sprite at", self.location
        draw_sprite(self.sprite, canvas, self.location)

class Environment(object):
    def draw(self, canvas):
        """Draw the environment."""

def main():
    master = Tkinter.Tk()
    master.title("Fishbowl")
    frame = Tkinter.Frame(master, width=800, height=600)
    frame.pack()
    canvas = Tkinter.Canvas(frame, width=800, height=600)
    canvas.grid(sticky="nw")
    master.resizable(0, 0)

if __name__ == "__main__":
    main()

