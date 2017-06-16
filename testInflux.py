#!/usr/bin/python

# A little script to send test data to an influxdb installation
# Attention, the non-core library 'requests' is used. You'll need to install it first:
# http://docs.python-requests.org/en/master/user/install/

import json
import math
from random import randint
import requests
import sys
from time import sleep

IP = "localhost"        # The IP of the machine hosting your influxdb instance
DB = "mydb"               # The database to write to, has to exist
#USER = "user"             # The influxdb user to authenticate with
#PASSWORD = "password123"  # The password of that user
TIME = 1                  # Delay in seconds between two consecutive updates
STATUS_MOD = 5            # The interval in which the updates count will be printed to your console

n = 0

for d in range(0,19):
    ## without autentication
    # v = "powermanagement,l1=" + str(randint(-5,5)) + ",l2=" + str(randint(-5,5)) + ",l3=" + str(randint(-5,5))
    v = randint(-5,5)
    r = requests.post("http://%s:8086/write?db=%s" %(IP, DB), data=v)
    if r.status_code != 204:
        print 'Failed to add point to influxdb (%d) - aborting.' %r.status_code
        sys.exit(1)
    print v
