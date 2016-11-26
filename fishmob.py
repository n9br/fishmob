#!/usr/bin/env python#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import ConfigParser
import RPi.GPIO as GPIO ## Import GPIO library

# configfile = "/etc/fishmob.cfg"
configfile = "/etc/fishmob.cfg"




parser = argparse.ArgumentParser(description="program controlling fishmob \n specify Action, PIN \n uses configfile in /etc")
parser.add_argument("action", help="read = read sensor, or control = control a device", type=str)
parser.add_argument("devicename", help="Name des Sensors oder des Geräts lt Section des config file", type=str)
parser.add_argument("--help, ")
args = parser.parse_args()

# initialize and read config
# Config wird eine Liste von Dictionaries
# ansprechbar via Config.items[Sectionname]
Config=ConfigParser.ConfigParser()
Config
Config.read(configfile)

# Sensor = key/value dict of properties
lSensor = Config.items(args.devicename)
Sensor = dict(lSensor)
print Sensor

# initialize mode; using  
GPIO.setmode(GPIO.BOARD)

# set direction of PINs (in/out)
pin = int(Sensor['pin'])
print Sensor['pin']
GPIO.setup(pin, GPIO.OUT) 
