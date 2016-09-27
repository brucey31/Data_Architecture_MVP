from __future__ import print_function
from botocore.vendored import requests
import csv
import json
import base64
import re

print('Loading function')
key = '7ce17c273559653b041e8df9e7f65716453ceffd'


def lambda_handler(event, context):
    iterator = 1
    list = []
    while iterator < 130:
        list.append(iterator)
        iterator = iterator + 1

    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record['kinesis']['data'])
        print(payload)
        paramstring = payload.split("\t")
        print(paramstring)

        if paramstring[4] == "struct":
            uid = paramstring[9]
            event = paramstring[20]
            ts = paramstring[1]
            unit_id = paramstring[22]
            package = paramstring[21]
            price = paramstring[23]
            platform = paramstring[0]

        request = requests.get(
            'https://trk.kissmetrics.com/e?_n=%s&_k=%s&_p=%s&_t=%s&price=%s&platform=%s&unit_id=%s&package=%s' % (
            event, key, uid, ts, price, platform, unit_id, package))
        if request.status_code == 200:
            success = "Sent %s, %s, %s, %s, %s, %s, %s" % (uid, event, ts, package, price, platform, unit_id)
            print(success)
        else:
            print('Something went wrong')

    return success