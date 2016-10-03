from intercom import User, Intercom, Event
import datetime

Intercom.app_id = "jl23wpxw"
Intercom.app_api_key = "aec63c27411c712cc34cbc663ab027c7a718c7e3"


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
