"""
GPL 3 License
Copyright (c) 2020 Samsung. n.herriot@samsung.com
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__version__ = '0.1.0'
__author__ = 'Nicholas Herriot'
__license__ = "GPL3"

from pyb import LED, Switch, Pin
from drivers.usonic.ultrasonic import Ultrasonic, MeasurementTimeout
import time
import ujson

# Create variables to control on board LED Lights.
led1 = LED(1)   # RED coloured LED
led2 = LED(2)   # Green coloured LED
led3 = LED(3)   # Blue coloured LED

# Create variable for the ultrasonic sensor.
sensor = Ultrasonic(Pin.board.X3, Pin.board.X4)

# Create variable which detects the USR button being pressed.
switch = Switch()

# Read configuration values from our json config file
config_file = open('config.json', 'r')
config = ujson.loads(config_file.read())
print("Config file read")
print("Pump controller version: {}".format(config['pump_controller_version']))
print("Pump sensor read time period is: {}".format(config['ultrasonic_time_period']))
time_period = config['ultrasonic_time_period']

print("***Starting pump controller! ****")
print("USR switch value is: {}".format(switch.value()))
counter = 1

while not switch.value():
    led2.toggle()
    print('*** Pump controller active! ***')

    if counter >= time_period:

        try:
            dist = sensor.distance_in_cm()
            print("Dist = {}".format(dist))
        except MeasurementTimeout as e:
            print("{}".format(e))
        counter = 1

    time.sleep(1)
    counter = counter + 1

print("USR switch value is: {}".format(switch.value()))
print("\n*** Pump controller stopped due to USR switch being pressed")
