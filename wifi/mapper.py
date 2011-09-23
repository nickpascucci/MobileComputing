#!/usr/bin/python
# Mapper.py - Mapping of Wifi signal

import Tkinter

corner_y = 38.85065
corner_x = -104.82943
y_conversion = 4.141e-6
x_conversion = 5.359e-6


def convert_to_pixels(lat, lon):
    delta_x = lon - corner_x
    delta_y = corner_y - lat
    pix_x = int(delta_x / x_conversion)
    pix_y = int(delta_y / y_conversion)
    return (pix_x, pix_y)

def populate_map(canvas, net_strength):
    for lat, lon in net_strength.iterkeys():
        tig_str, guest_str = net_strength[(lat, lon)]
        center_x, center_y = convert_to_pixels(lat, lon)
        color = "green"
        if tig_str > -90 and tig_str < -80:
            color = "yellow"
        elif tig_str < -90:
            color = "red"
        canvas.create_oval(center_x - 10, center_y - 10, center_x + 10, center_y + 10, outline=color)
        color = "green"
        if guest_str > -90 and guest_str < -80:
            color = "yellow"
        elif guest_str < -90:
            color = "red"
        canvas.create_rectangle(center_x - 7, center_y - 7, center_x + 7, center_y + 7, outline=color)

def parse_data(data_file):
    net_strength = {}
    for line in data_file:
        line = line.replace(",", "") # Remove all commas, as they are unnecessary
        line = line.replace("(", "")
        line = line.replace(")", "")
        tokens = line.split(" ")
        try:
            lat = float(tokens[0])
            lon = float(tokens[1])
        except:
            continue
        maxes = find_max(tokens[2:])
        net_strength[(lat, lon)] = maxes
    return net_strength

def find_max(tokens):
    tig2_max = -1000
    guest_max = -1000
    for i in range(0, len(tokens), 3):
        sig_str = int(tokens[i+2])
        if tokens[i] == "tigernet2":
            if sig_str > tig2_max:
                tig2_max = sig_str
        if tokens[i] == "ccguest":
            if sig_str > guest_max:
                guest_max = sig_str
    return (tig2_max, guest_max)

def main():
    data_file = open("WifiData.txt", "r")
    net_strength = parse_data(data_file)
    master = Tkinter.Tk()
    master.title("Map")
    frame = Tkinter.Frame(master, width=1280, height=1280)
    frame.pack()
    canvas = Tkinter.Canvas(frame, width=1280, height=1280)
    canvas.grid(sticky="nw")
    master.resizable(0, 0)
    map_image = Tkinter.PhotoImage(file="map.gif")
    canvas.create_image(640, 640, image=map_image)
    populate_map(canvas, net_strength)
    frame.mainloop()

if __name__ == "__main__":
    main()
