from intercom import User, Intercom, Event
import datetime
import ConfigParser

config = ConfigParser.ConfigParser()
ini = config.read('conf2.ini')

INTERCOM_APP_ID = config.get('INTERCOM', 'ID')
INTERCOM_API_KEY = config.get('INTERCOM', 'KEY')


Intercom.app_id = INTERCOM_APP_ID
Intercom.app_api_key = INTERCOM_API_KEY


try:
    user = User.find(email="customer3@example.com")
    print "Found Email"

except:
    user = User.create(email="customer3@example.com", name="Janet Doe")
    print "Created new email"
# print user.custom_attributes["Browser"]

timestamp= int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds())
Event.create(
    event_name="Bruce_test",
    created_at=timestamp,
    email=user.email,
    metadata={
        "Params": "test-test",
        "timestamp": timestamp
    }
)
