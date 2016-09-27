from __future__ import print_function
from botocore.vendored import requests
import base64

print('Loading function')
key = '7ce17c273559653b041e8df9e7f65716453ceffd'


def lambda_handler(event, context):
    for record in event['Records']:

        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record['kinesis']['data'])
        print(payload)

        # Change from tab delimited to dict
        paramstring = payload.split("\t")

        # Grab the fields I want
        if paramstring[5] == "struct":
            event = paramstring[54]
            ts = paramstring[2]
            unit_id = paramstring[56]
            package = paramstring[55]
            price = paramstring[57]
            platform = paramstring[1]
            uid = paramstring[12]

            # Ping to KISSMETRICS
            request = requests.get(
                'https://trk.kissmetrics.com/e?_n=%s&_k=%s&_p=%s&_t=%s&price=%s&platform=%s&unit_id=%s&package=%s' % (
                event, key, uid, ts, price, platform, unit_id, package))
            if request.status_code == 200:
                success = "Sent %s, %s, %s, %s, %s, %s, %s" % (uid, event, ts, package, price, platform, unit_id)
                print(success)
            else:
                print('Something went wrong')

            return success

        else:
            continue