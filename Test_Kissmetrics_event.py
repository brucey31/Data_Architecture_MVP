import requests
import csv
import time


key = '7ce17c273559653b041e8df9e7f65716453ceffd'


bruce = "awesome"
while bruce == "awesome" :
    with open('Kinesis_Test_Data.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            event_name = row[0]
            unit_id = row[1]
            package = row[2]
            price = row[3]
            platform = row[4]
            uid = row[5]
            ts = int(time.time())

            request = requests.get('https://trk.kissmetrics.com/e?_n=%s&_k=%s&_p=%s&_t=%s&price=%s&platform=%s&unit_id=%s&package=%s' % (event_name, key, uid, ts, price, platform, unit_id, package))
            if request.status_code == 200:
                print "Sent %s, %s, %s, %s, %s, %s, %s" % (uid, event_name, ts, package, price, platform, unit_id)
            else:
                print 'Something went wrong'
