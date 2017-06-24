from influxdb import InfluxDBClient
import csv
import json

query = "select mean(*) from power where time < now() group by time(1m) fill(none);"
client = InfluxDBClient('localhost', 8086, 'root', 'root', 'logging')
result = client.query(query)
rows = json.loads(result)
with open('test.csv', 'wb+') as f:
    dict_writer = csv.DictWriter(f, fieldnames=['time', 'l1', 'l2', 'l3'])
    dict_writer.writeheader()
    dict_writer.writerows(rows)
