# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient
import csv
import json

query = 'SELECT "dachs1" AS "Dachs 1", "dachs2" AS "Dachs 2", "oil_dachs" AS "Öldachs", "oil1" AS "Öl 1", "oil2" AS "Öl 2" FROM "burner" where time < now() - 1m group by time(1m) fill(none);'
client = InfluxDBClient('localhost', 8086, 'root', 'root', 'logging')
result = client.query(query)

with open('test.csv', 'wb+') as f:
    with open('query.csv', 'w') as f: 
        f.write('day;time;l1;l2;l3');
        for i in result.get_points('power'):
            row = '\n' + str(i['time'])[0:10] + ';' + str(i['time'])[11:-1] + ';' + str(i['mean_l1']) + ';' +  str(i['mean_l2']) + ';' + str(i['mean_l3'])
            f.write(row) 
    
    
