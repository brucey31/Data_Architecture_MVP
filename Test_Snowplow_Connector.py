from snowplow_tracker import Subject, Tracker, Emitter
import urllib2
import csv
import time
import calendar
import datetime

app_id = 'Busuu'
e = Emitter("10.0.52.22", port=8080)
t = Tracker(e, app_id=app_id, encode_base64=True)


ret = urllib2.urlopen('https://enabledns.com/ip')
ip = ret.read()

bruce = "awesome"
while bruce == "awesome":
    with open('Kinesis_Test_Data.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            event_name = row[0]
            unit_id = row[1]
            package = row[2]
            price = row[3]
            platform = "pc"
            uid = row[5]
            timestamp = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)

            # Set params for specific User
            s = Subject()
            t.subject.set_platform(platform).set_user_id(uid).set_lang("enc").set_ip_address(ip)

            # Send it to emitter
            # t.track_struct_event("test", event_name, package, unit_id, float(price), None, calendar.timegm(time.gmtime()))
            t.track_struct_event(event_name, package, unit_id, price, None, None, timestamp)

            t.track_page_view("https://www.busuu.com/en/learn/start-learning/", "Enc Landing page", "https://www.busuu.com/en/learn/start-learning/?b_source=adwords&b_campaign=uk_en_web_brand_e&b_group=uk_en_web_brand_e&b_subnetwork=sn&b_term=busuu&b_placement=&utm_nooverride=1&gclid=CL-D_ajzr88CFU6eGwodq_YHzw")


