# testing string for base64 encoded string = QnVzdXUJcGMJMjAxNi0xMC0wMyAxNTo1OToxOS40MzcJMjAxNi0xMC0wMyAxNTo1OToxNC4yNzYJMjAxNi0xMC0wMyAxNTo1OToxNC4zMTQJc3RydWN0CTEwMWFkOWMxLTA3OGQtNDQ2NC05YjMyLTYxMzg2YzA3ZTJkMgkJCXB5LTAuNy4yCXNzYy0wLjYuMC1raW5lc2lzCWtpbmVzaXMtMC44LjEtY29tbW9uLTAuMjMuMQkxMjM0NTY4MjkJMTk1LjExMC42OS44NgkJCQllY2VkMDY5Mi0wY2RjLTQ2ZjMtOGNmZi0yNWY3ODdkZDQ2NTgJR0IJSDkJTG9uZG9uCUVDNE4JNTEuNTE0MjA2CS0wLjA5MzA5Mzg3CUxvbmRvbgkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJdXNlcl9yZWdpc3RlcmVkCWVuYwllcwl7J3NvdXJjZSc6ICdhZHdvcmRzJywgJ3Rlcm0nOiAnbGVhcm4gc3BhbmlzaCcsICdncm91cCc6ICdVS19JUkUnLCAnZW1haWwnOiAnMTIzNDU2ODI5QGJ1c3V1LmNvbScsICdjYW1wYWlnbic6ICdlbmNfYnJhbmQnfQkJCQkJCQkJCQkJCQkJCQkJCQkJCXB5dGhvbi1yZXF1ZXN0cy8yLjExLjEJCQkJCQllbmMJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCUV1cm9wZS9Mb25kb24JCQkJCQkJCQkyMDE2LTEwLTAzIDE1OjU5OjE0LjI3Ngljb20uZ29vZ2xlLmFuYWx5dGljcwlldmVudAlqc29uc2NoZW1hCTEtMC0wCQk=
from __future__ import print_function
from intercom import User, Intercom, Event
import datetime
import base64
import json

print('Loading function')


def lambda_handler(event, context):

    Intercom.app_id = {Insert here}
    Intercom.app_api_key = {Insert here}

    for record in event['Records']:

        # Kinesis data is base64 encoded so decode here
        print(record['kinesis']['data'])
        payload = base64.b64decode(record['kinesis']['data'])

        # Change from tab delimited to dict
        paramstring = payload.split("\t")
        print(paramstring)

        # Grab the fields I want
        if paramstring[5] == "struct" and paramstring[53] != "page_view":
            print("entered struct clause")
            event = paramstring[53]
            language_learnt = paramstring[55]
            interface_language = paramstring[54]
            platform = paramstring[1]
            params = paramstring[56]
            params = json.loads(params.replace("'", '"'))
            # print(event)
            # print(ts)
            # print(language_learned)
            # print(interface_language)
            # print(platform)
            # print(uid)
            # print(params)

            params_data = {}
            for param in params:
                params_data[param] = params[param]

            params_data["language_learnt"] = language_learnt
            params_data["interface_language"] = interface_language
            params_data["platform"] = platform

            email = params_data["email"]

            # params_data = json.dumps(params_data)
            print(params_data)

            try:
                user = User.find(email=email)

            except:
                user = User.create(email=email)

            # Ping to Intercom
            timestamp = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds())
            Event.create(
                event_name=event,
                created_at=timestamp,
                email=user.email,
                metadata=params_data
            )

        else:
            continue
