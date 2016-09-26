from __future__ import print_function
import base64
import json
import boto3
import json
import re

print('Loading function')
firehoseClient = boto3.client('firehose')
streamName = 'rawdata'


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record['kinesis']['data'])
        print(payload)
        # inputed = json.dumps({'data': payload })
        line = re.sub("\t", ",", payload)
        line2 = re.sub("app_1", "\napp_1", line)[:-2]
        dict_1 = {"Data": line2}
        print(dict_1)
        SendToFireHose(streamName, dict_1)
        success = "Sent data sucessfully Wahoo!!"
        print(success)


def SendToFireHose(streamName, record):
    response = firehoseClient.put_record(
        DeliveryStreamName=streamName,
        Record=record
    )