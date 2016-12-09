#!/usr/bin/env python#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import ConfigParser
import datetime
# import RPi.GPIO as GPIO ## Import GPIO library
import sqlite3 as lite
import sys


parser = argparse.ArgumentParser(description="getting sensor data for fishmob \n specify sensor in configfile")
# parser.add_argument("devicename", help="Name des Sensors lt Section des config file", type=str)
parser.add_argument("--help, ")
args = parser.parse_args()

now = datetime.datetime.now()
# configfile = "/etc/fishmob.cfg"
configfile = "/etc/fishmob/sensors.cfg"
dbname = str(now.year)+str(now.month)+'.db'


# initialize and read config
# Config wird eine Liste von Dictionaries
# ansprechbar via Config.items[Sectionname]
Config=ConfigParser.ConfigParser()
Config
Config.read(configfile)

# Sensor = key/value dict of properties
<<<<<<< HEAD
lSensor = Config.items(args.devicename)
Sensor = dict(lSensor)
print Sensor

# initialize mode; using
# GPIO.setmode(GPIO.BOARD)

# set direction of PINs (in/out)
# pin = int(Sensor['pin'])
# print Sensor['pin']
# GPIO.setup(pin, GPIO.OUT)
=======
for section in Config.sections():
    print Config.items(section)
>>>>>>> master
