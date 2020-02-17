# Bulb API backend
"""
Author: Simon Laffan
Created: 12/02/2020
Updated: 12/02/2020
Version: 0.0.1
https://github.com/Blahnacles
"""
# imports
from flask import Flask, jsonify, request, escape
import yeelight, json
from yeelight import Bulb

# setup
# Hardcoding IP for now, as discover_bulbs() does not work
bedroom_ip = "192.168.1.122"
bedroom = Bulb(bedroom_ip)
if bedroom.get_properties()['music_on']== '0':
    try:
        bedroom.start_music(port=5555)
    except yeelight.BulbException:
        pass


app = Flask(__name__)
@app.route("/api", methods=['GET'])
def get_status(): 
    return json.dumps(Bulb(bedroom_ip).get_properties())


if __name__ == '__main__':
    app.run(host='0.0.0.0')