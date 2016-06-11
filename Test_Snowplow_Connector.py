from snowplow_tracker import Subject, Tracker, Emitter
from snowplow_tracker import SelfDescribingJson
import csv
import time

e = Emitter("10.0.52.22", port=8080)
t = Tracker(e)
s = Subject()


while 1 == 1 :
    with open('Kinesis_Test_Data.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            event_name = row[0]
            unit_id = row[1]
            package = row[2]
            price = row[3]
            platform = row[4]
            uid = row[5]

            s.set_platform("pc").set_user_id(uid).set_lang("enc")

            t.track_unstruct_event(SelfDescribingJson(
                "com.example_company/save-game/jsonschema/1-0-2",
                {"event": event_name,
                "package": package,
                "unit_id": unit_id,
                "price": price,
                "timestamp": str(time.strftime("%Y-%m-%d %H:%m:%S"))
                }))
