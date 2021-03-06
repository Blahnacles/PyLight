# Bulb UI script - allows control of buttons from a tkinter interface
# In future may be replaced with CSS or some other UI wrapper
"""
Author: Simon Laffan
Created: 13/01/2020
Updated: 13/01/2020
Version: 0.0.1
https://github.com/Blahnacles
"""
# Setup
# Imports
from tkinter import *
# Hardcoding IP for now, as discover_bulbs() does not work
bedroom_ip = "192.168.1.122"
update_rate = 2000 # UI refresh rate in ms
# TODO set static ip
import yeelight
from yeelight import Bulb
global bedroom
bedroom = Bulb(bedroom_ip)
bedroom.start_music(port=5555)
bedroom_data = bedroom.get_properties()


# setup window
window = Tk()
window.title("PySwitch")
#window.geometry('800x480')

# setup buttons & labels
switch_text = "+"
switch_bg = "black"
switch_fg = "orange"
if bedroom_data['power']=='on':
    switch_text = "-"
    switch_bg = "orange"
    switch_fg = "black"

light_switch_button = Button(window, text=switch_text, font=("fixedsys", 50), bg=switch_bg, fg=switch_fg)
# exit button
exit_button = Button(window, text=X, font=("fixedsys", 50), bg="red", fg="black")
# brightness scale
brightness_scale = Scale(window, from_=100, to=0)
# blue button
blue_button = Button(window, text="Blue", highlightbackground="blue", bg="blue")
# white button
white_button = Button(window, text="White", highlightbackground="white", bg="white")
# red button
red_button = Button(window, text="Red", highlightbackground="red", bg="red")

# setup functions for interaction
def switch_update(bedroom_data):
    if bedroom_data['power']=='on':
        switch_text = "-"
        switch_bg = "orange"
        switch_fg = "black"
    else:
        switch_text = "+"
        switch_bg = "black"
        switch_fg = "orange"
    light_switch_button.config(text=switch_text, bg=switch_bg, fg=switch_fg)

def bedroom_toggle():
    global bedroom
    # Toggles lights, formats button appropriately
    bedroom.toggle()
    #bedroom_data = bedroom.get_properties()
    if bedroom_data['power']=='on':
        bedroom_data['power']='off'
    else:
        bedroom_data['power']='on'
    switch_update(bedroom_data)
    

def refresh():
    global bedroom
    # periodic refresh function, to sync with mobile controllers
    # refresh for light switch:
    try:
        bedroom_data = bedroom.get_properties()
        switch_update(bedroom_data)
    except yeelight.main.BulbException:
        print("exception handled appropriately")
        # reinstantiating bulb
        bedroom = Bulb(bedroom_ip)
    window.after(update_rate,refresh)

def brightness_callback(b):
    global bedroom
    print(b)
    #bedroom.set_brightness(b)
    try:
        bedroom.set_brightness(int(b))
    except yeelight.main.BulbException:
        bedroom = Bulb(bedroom_ip)

def set_colour(r,g,b):
    bedroom.turn_on()
    bedroom.set_rgb(r,g,b)



# add functions to buttons
light_switch_button.config(command=bedroom_toggle)
exit_button.config(command=window.destroy)
brightness_scale.config(command=brightness_callback)
red_button.config(command=lambda: set_colour(255,0,0))
blue_button.config(command=lambda: set_colour(0,0,255))
white_button.config(command=lambda: set_colour(255,255,255))
# place buttons & labels
#light_switch_button.pack(anchor=CENTER)
#brightness_scale.pack(anchor=CENTER)
#exit_button.pack(anchor=CENTER)
exit_button.grid(column=2,sticky=E)
light_switch_button.grid(row=1,column=0, rowspan=3)
brightness_scale.grid(row=1,column=1, rowspan=3)
red_button.grid(row=1,column=2)
blue_button.grid(row=2,column=2)
white_button.grid(row=3,column=2)
# update UI widgets periodically
window.after(update_rate,refresh)
window.mainloop()
