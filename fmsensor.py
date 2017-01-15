#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import ConfigParser
import datetime
import logging
# import RPi.GPIO as GPIO ## Import GPIO library
import os
import platform
import sqlite3 as lite
import sys

# con None
# dbdir = "/var/lib/fishmob/"
# dbdir = "~/.fishmob/"
configfile = "/etc/fishmob/fishmob.cfg"
sensorsfile = "/etc/fishmob/sensors.cfg"

# logging.basicConfig(level=logging.WARNING)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser(description="getting sensor data for fishmob \n specify sensor in configfile %s" % sensorsfile)
# parser.add_argument("devicename", help="Name des Sensors lt Section des config file", type=str)
parser.add_argument("--help, ")
args = parser.parse_args()

now = datetime.datetime.now()

# initialize and read config
# fConfig wird eine Liste von Dictionaries, ansprechbar via Config.items[Sectionname]
fConfig=ConfigParser.ConfigParser()
fConfig
logger.info('reading general config')
try:
    fConfig.read(configfile)
except:
    logger.error('Failed to read ' + configfile)

try:
    dCommon = dict(fConfig.items('Common'))
except:
    logger.error('Cant\'t read dbdir from %s' % configfile)

# Check DB Location and open
dbdir = dCommon['dbdir']
if not dbdir.endswith('/'):
    dbdir = dbdir + '/'
dbdir = os.path.expanduser(dbdir)
logger.info('dbdir is ' + dbdir)
dbname = dbdir + str(now.year) + str(now.month).zfill(2) + '.db'
# sDate = str(now.date())
# print sDate


# initialize and read sensorconfig
# Config wird eine Liste von Dictionaries, ansprechbar via Config.items[Sectionname]
fSensors=ConfigParser.ConfigParser()
# create instance
fSensors
logger.info('reading sensors config')
try:
    fSensors.read(sensorsfile)
except:
    logger.error('Failed to read ' + sensorsfile)

# dbDir prüfen
try:
    if not os.path.exists(dbdir):
        os.makedirs(dbdir)
except (SystemExit, KeyboardInterrupt):
    raise
except Exception, e:
    logger.error('Failed to create directory' + dbdir, exc_info=True)


# DB connection
try:
    con = lite.connect(dbname)
except (SystemExit, KeyboardInterrupt):
    raise
except Exception, e:
    logger.error('Failed to open file' + dbname, exc_info=True)

cur = con.cursor()


for section in fSensors.sections():
    itemlist = dict(fSensors.items(section))          # Sensor = key/value dict of properties
#    print section
    if not platform.machine() == 'armv7l':
        import random
        random.seed()
        degrees = str(random.uniform(-5,30))
        hectopascals = random.uniform(1000,1020)
        humidity = random.uniform(30,99)
        print 'Temp      = {0:0.3f} deg C'.format(float(degrees))
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
        (date date, hour int, min int, hum real, press real, temp real )'.format(tn=section))
#        (date text, hour int, min int, hum real, press real, temp real )'.format(tn=section))


#   insert Data
    cur.execute("INSERT INTO {tn} VALUES (date('now','localtime'),{hr},{min},{hum},{press},{temp})".\
        format(tn=section, hr=now.hour, min=now.minute, hum=humidity, press=hectopascals, temp=degrees))
#        format(tn=section, dt=sDate, hr=now.hour, min=now.minute, hum=humidity, press=hectopascals, temp=degrees))
#    cur.execute("INSERT INTO TempSensor1 VALUES ('2016-12-21','08','07')")

#    try:
#        cur.execute('INSERT INTO {tn} VALUES ('2016-12-20',now.hour,now.min)'.format(tn=section))
#    except sqlite3.IntegrityError:
#        print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))


con.commit()
if con:
    con.close()
