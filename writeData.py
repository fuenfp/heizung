import socket
import sys
from influxdb import InfluxDBClient
from datetime import datetime
from struct import unpack

def write_power_data(l1, l2, l3, time):
    json_body = [
        {
            "measurement": "power",
            "time": time,
            "fields": {
                "l1": l1,
                "l2": l2,
                "l3": l3
            }
        }
    ]
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'logging')
    client.create_database('logging')
    client.write_points(json_body)
    result = client.query('select * from power;')
    print("Result: {0}".format(result))

while True:

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('172.16.50.10', 1026)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    #sock.sendall('ready for receiving :-)')
    try:
        while True:
            d = unpack('fff',sock.recv(12))
            print d
            write_power_data(d[0],d[1],d[2], datetime.now())  
    except (KeyboardInterrupt, SystemExit):
        raise        
    except:
        pass;
    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()
