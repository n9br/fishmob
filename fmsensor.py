#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
import argparse
import ConfigParser
import datetime
# import RPi.GPIO as GPIO ## Import GPIO library
import sqlite3 as lite
import sys

# con None
configfile = "/etc/fishmob/sensors.cfg"


parser = argparse.ArgumentParser(description="getting sensor data for fishmob \n specify sensor in configfile %s" % configfile)
# parser.add_argument("devicename", help="Name des Sensors lt Section des config file", type=str)
parser.add_argument("--help, ")
args = parser.parse_args()

now = datetime.datetime.now()
dbname = str(now.year)+str(now.month)+'.db'


# initialize and read config
# Config wird eine Liste von Dictionaries
# ansprechbar via Config.items[Sectionname]
Config=ConfigParser.ConfigParser()
# create instance
Config
Config.read(configfile)

con = lite.connect(dbname)
cur = con.cursor()


for section in Config.sections():
    itemlist = dict(Config.items(section))          # Sensor = key/value dict of properties
#   if itemlist['category'] == "Temp": kann später eingegrenzt werden

    if not platform.machine() == 'armv7l':
        next;
    else:

## adjust values
        if itemlist['type'] == "BME280":
            from Adafruit_BME280 import *

            sensor = BME280(mode=BME280_OSAMPLE_8)
            degrees = sensor.read_temperature
            pascals = sensor.read_pressure()
            hectopascals = pascals / 100
            humidity = sensor.read_humidity()
            print 'Sensor    = %'.format(section)
            print 'Temp      = {0:0.3f} deg C'.format(degrees)
            print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
            print 'Humidity  = {0:0.2f} %'.format(humidity)

 ##   get values  -> hand PIN / address ??
    print section
    #cur.execute('''CREATE TABLE IF NOT EXISTS section (date text, hour int, min int, hum real, press real, temp real )''')
# create table if not exists
    cur.execute('''CREATE TABLE IF NOT EXISTS '
        + section
        + ' (date text, hour int, min int, hum real, press real, temp real )''');
    ## check if need to create table like
    #cur.execute(""" SELECT COUNT(*) FROM sqlite_master WHERE name = ?  """, (section, ))
    #if not cursor.fetchone():
    #    cur.execute('''CREATE TABLE ? )

con.commit()
if con:
    con.close()