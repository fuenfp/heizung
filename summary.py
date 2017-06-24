from influxdb import InfluxDBClient
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

def write_summary_data(l1, l2, l3, mode, time):
    json_body = [
        {
            "measurement": "power_summary",
            "time": str(time),
            "tags":{
                "mode" : mode
            },
            "fields": {
                "l1": l1,
                "l2": l2,
                "l3": l3,
                "sum": l1 + l2 + l3
            }
        }
    ]
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'logging')
    #print json_body
    client.create_database('logging')
    client.write_points(json_body)


def getSummaryOfDay(day):
    next_day = day +  timedelta(1)
    query = "select mean(*) from power where time > '" + str(day) + "' and time < '" + str(next_day) + "' group by time(1m) fill(none);"
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'logging')
    result = client.query(query)
    gekauft_l1 = 0.0
    verkauft_l1 = 0.0
    gekauft_l2 = 0.0
    verkauft_l2 = 0.0
    gekauft_l3 = 0.0
    verkauft_l3 = 0.0

    for i in result.get_points('power'):
        l1 = i['mean_l1']/60
        l2 = i['mean_l2']/60
        l3 = i['mean_l3']/60

        if l1 > 0:
            gekauft_l1 = gekauft_l1 + l1
        else:
            verkauft_l1 = verkauft_l1 + l1
        if l2 > 0:
            gekauft_l2 = gekauft_l2 + l2
        else:
            verkauft_l2 = verkauft_l2 + l2
        if l3 > 0:
            gekauft_l3 = gekauft_l3 + l3
        else:
            verkauft_l3 = verkauft_l3 + l3
         
  
    #print str(day)
    #print 'gekauft: l1: ' + str(gekauft_l1)   + ' l2: ' + str(gekauft_l2)  + 'l3: ' + str(gekauft_l3)  + ' sum:' + str(gekauft_l1 + gekauft_l2 + gekauft_l3)
    write_summary_data(gekauft_l1, gekauft_l2, gekauft_l3, "gekauft", day)
    #print 'verkauft: l1: ' + str(verkauft_l1) + ' l2: ' + str(verkauft_l2) + 'l3: ' + str(verkauft_l3) + ' sum:' + str(verkauft_l1 + verkauft_l2 + verkauft_l3)
    #write_summary_data(verkauft_l1, verkauft_l2, verkauft_l3, "verkauft", day)
    return [gekauft_l1,gekauft_l2,gekauft_l3, verkauft_l1,verkauft_l2,verkauft_l3]


def getSummaryOfMonth(month, year):
    current_day = datetime(year,month,1)
    last = datetime(2017,1,1) + relativedelta(months=1)
    print "summary of month: " + str(month)

    while current_day < last:
       tmp = getSummaryOfDay(current_day)
       for i in xrange(0,len(tmp)-1):
          last[i] = tmp[i] + last[i]      
       current_day = current_day + timedelta(days=1)
       

    print "gekauft: " + str(last[0] + last[1] + last[2])
    print "verkauft:" + str(last[3] + last[4] + last[5])
    

getSummaryOfMonth(1,2017)    
print 'finish! :-)'
