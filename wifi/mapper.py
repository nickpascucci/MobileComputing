# Mapper.py - Mapping of Wifi signal

import Tkinter

data_file = open("WifiData.txt", "r")
corner_y = 38.85065
corner_x = -104.82943
y_conversion = 4.141e-6
x_conversion = 5.359e-6

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

def convert_to_pixels(lat, lon):
    delta_x = lon - corner_x
    delta_y = corner_y - lat
    pix_x = int(delta_x / x_conversion)
    pix_y = int(delta_y / y_conversion)
    return (pix_x, pix_y)

net_strength = {}

for line in data_file:
    line = line.replace(",", "") # Remove all commas, as they are unnecessary
    line = line.replace("(", "")
    line = line.replace(")", "")
    print line
    tokens = line.split(" ")
    try:
        lat = float(tokens[0])
        lon = float(tokens[1])
    except:
        continue
    maxes = find_max(tokens[2:])
    print lat, lon, ":", maxes[0], maxes[1]
    net_strength[(lat, lon)] = maxes

master = Tkinter.Tk()
master.title("Map")
frame = Tkinter.Frame(master, width=1280, height=1280)
frame.pack()
canvas = Tkinter.Canvas(frame, width=1280, height=1280)
canvas.grid(sticky="nw")
master.resizable(0, 0)

map_image = Tkinter.PhotoImage(file="map.gif")
canvas.create_image(640, 640, image=map_image)
for lat, lon in net_strength.iterkeys():
    map_image.put(data="#FF0000", to=convert_to_pixels(lat, lon))
frame.mainloop()
