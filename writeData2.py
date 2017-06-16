import socket
import sys
import time
from influxdb import InfluxDBClient
from datetime import datetime
from struct import unpack

def write_power_data(l1, l2, l3, time):
    json_body = [
        {
            "measurement": "power",
            #"time": time,
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

def write_temperature_data(t, time):
    json_body = [
        {
            "measurement": "temperature",
            #"time": time,
            "fields": {
                "outside": t[0],
                "fro_Boiler": t[1],
                "fro_Exhaust": t[2],
                "eta_Boiler": t[3],
                "eta_Exhaust": t[4],
                "oil1": t[5],
                "oil2": t[6],
                "ab_hc_supply": t[7],
                "ab_warmwater":t[8],
                "ba2_hc_supply": t[9],
                "ba2_warmwater": t[10],
                "ba3_hc_supply": t[11],
                "buffer_upper": t[12],
                "buffer_2upper": t[13],
                "buffer_2lower": t[14],
                "buffer_lower": t[15]
            }
        }
    ]
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'logging')
    client.create_database('logging')
    client.write_points(json_body)

def write_burner_data(t, time):
    json_body = [
        {
            "measurement": "burner",
            #"time": time,
            "fields": {
                "dachs1": t[0],
                "dachs2": t[1],
                "oil_dachs": t[2],
                "oil1": t[3],
                "oil2": t[4],
                "froeling": t[5],
                "eta": t[6]
            }
        }
    ]
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'logging')
    client.create_database('logging')
    client.write_points(json_body)



while True:
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('172.16.50.10', 1028)
        print >>sys.stderr, 'connecting to %s port %s' % server_address
        sock.connect(server_address)
        sock.sendall('ready for receiving :-)')
        while True:
            data = sock.recv(84)
            print len(data)
            d = unpack('fffffffffffffffffff????????',data)
            print d
            write_power_data(d[0],d[1],d[2], datetime.now())
            write_temperature_data(d[3:19], datetime.now())
            write_burner_data(d[19:26], datetime.now())  
    except (KeyboardInterrupt, SystemExit):
        raise        
    except:
        pass;
    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()
        time.sleep(5)
