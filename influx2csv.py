# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient
import csv
import json

query = "select * from burner where time < now() - 1m;"
client = InfluxDBClient('localhost', 8086, 'root', 'root', 'logging')
result = client.query(query)

with open('test.csv', 'wb+') as f:
    with open('query.csv', 'w') as f: 
        f.write('day;time;l1;l2;l3');
        for i in result.get_points('burner'):
            row = '\n' + str(i['time'])[0:10] + ';' + str(i['time'])[11:-1] + ';' + str(i['oil_dachs']) + ';' + str(i['dachs1']) + ';' +  str(i['dachs2'])
            f.write(row) 
    
    
