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
sDate = str(now.date())
print sDate


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
#    print section
    if not platform.machine() == 'armv7l':
        import random
        random.seed()
        degrees = random.uniform(-5,30)
        hectopascals = random.uniform(1000,1020)
        humidity = random.uniform(30,99)
        print 'Temp      = {0:0.3f} deg C'.format(degrees)
        print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
        print 'Humidity  = {0:0.2f} %'.format(humidity)
#        next;
    else:

## adjust values
        if itemlist['type'] == "BME280":
            from Adafruit_BME280 import *

            sensor = BME280(mode=BME280_OSAMPLE_8)
            degrees = sensor.read_temperature
            pascals = sensor.read_pressure()
            hectopascals = pascals / 100
            humidity = sensor.read_humidity()
            print 'Sensor    = {sens}'.format(sens=section)
            print 'Temp      = {0:0.3f} deg C'.format(degrees)
            print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
            print 'Humidity  = {0:0.2f} %'.format(humidity)
#   create table if non-existent
    cur.execute('CREATE TABLE IF NOT EXISTS {tn} \
        (date text, hour int, min int, hum real, press real, temp real )'.format(tn=section))

#   insert Data
    cur.execute("INSERT INTO {tn} VALUES ({dt},{hr},{min},{hum},{press},{temp})".\
        format(tn=section, dt=sDate, hr=now.hour, min=now.minute, hum=humidity, press=hectopascals, temp=degrees))
#    cur.execute("INSERT INTO TempSensor1 VALUES ('2016-12-21','08','07')")

#    try:
#        cur.execute('INSERT INTO {tn} VALUES ('2016-12-20',now.hour,now.min)'.format(tn=section))
#    except sqlite3.IntegrityError:
#        print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))


con.commit()
if con:
    con.close()
