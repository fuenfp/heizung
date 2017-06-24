from influxdb import InfluxDBClient
import csv
import json

query = "select mean(*) from power where time < now() - 1m group by time(1m) fill(none);"
client = InfluxDBClient('localhost', 8086, 'root', 'root', 'logging')
result = client.query(query)

with open('test.csv', 'wb+') as f:
    with open('query.csv', 'w') as f: 
        f.write('time;l1;l2;l3');
        for i in result.get_points('power'):
            row = '\n' + str(i['time'])[0:-1] + ';'str(i['mean_l1']) + ';' +  str(i['mean_l2']) + ';' + str(i['mean_l3'])
            f.write(row) 
    
    
