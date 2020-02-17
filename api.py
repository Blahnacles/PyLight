# Bulb API backend
"""
Author: Simon Laffan
Created: 12/02/2020
Updated: 12/02/2020
Version: 0.0.1
https://github.com/Blahnacles

To access on local machine: http://192.168.1.106:5000/api
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
@app.route("/api", methods=['GET','POST'])
def handle():
    if request.method == 'GET':
        return json.dumps(Bulb(bedroom_ip).get_properties())
    elif request.method == 'POST':
        try:
            bright = request.form['brightness']
            if bright < 101 and bright > -1:
                Bulb(bedroom_ip).set_brightness(int(bright))
            elif bright is None:
                app.logger.error('no brightness value received')
        except:
            app.logger.error('generic brightness error')
        try:
            if request.form['toggle'] is "true":
                Bulb(bedroom_ip).toggle() 
        except:
            app.logger.error('generic toggle error')



if __name__ == '__main__':
    app.run(host='0.0.0.0')