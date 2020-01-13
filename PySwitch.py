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
bedroom_data = bedroom.get_properties()


# setup window
window = Tk()
window.title("PySwitch")
window.geometry('800x480')

# setup buttons & labels
switch_text = "+"
switch_bg = "black"
switch_fg = "orange"
if bedroom_data['power']=='on':
    switch_text = "-"
    switch_bg = "orange"
    switch_fg = "black"

light_switch_button = Button(window, text=switch_text, font=("fixedsys", 50), bg=switch_bg, fg=switch_fg)

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



# add functions to buttons
light_switch_button.config(command=bedroom_toggle)
# place buttons & labels
light_switch_button.grid(column=1,row=0)
# TODO make exit button -> window.destroy
# update UI widgets periodically
window.after(update_rate,refresh)
window.mainloop()
