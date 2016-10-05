import json
from datetime import datetime
import requests
import ConfigParser

config = ConfigParser.ConfigParser()
ini = config.read('conf2.ini')

APPBOY_APP_ID = config.get('APPBOY', 'APP_ID')
APPBOY_APP_GROUP_ID = config.get('APPBOY', 'APP_GROUP_ID')

ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z%z')
print ts

url = 'https://api.appboy.com/users/track'

event_array = [{"external_id": "32767377",  "app_id": APPBOY_APP_ID, "name": "Bruce_test", "time": ts}]
headers = {"Content-Type": "application/json"}
data = {"app_group_id": APPBOY_APP_GROUP_ID, "events": event_array}

data_to_app = json.dumps(data)

r = requests.post(url,  data=data_to_app, headers=headers)

if r.status_code == 200:
    print "Sent Successfully"
else:
    print r.content