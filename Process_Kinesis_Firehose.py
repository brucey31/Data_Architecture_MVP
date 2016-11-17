from __future__ import print_function

import base64
import json
import boto3
import re

print('Loading function')
firehoseClient = boto3.client('firehose')


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    for record in event['Records']:
        print(record['kinesis']['data'])
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record['kinesis']['data'])
        print(payload)

        # TSV to CSV
        jsons = re.sub("{", '"{', payload)
        jsons2 = re.sub("}", '}"', jsons)
        line = re.sub("\t", ",", jsons2)
        line2 = re.sub("Busuu", "\nBusuu", line)
        line2 = re.sub("\"\"", "\"", line)
        print(line2)

        # Break down params json 56
        paramstring = payload.split("\t")

        if paramstring[56] and paramstring[56] != "":
            event_id = paramstring[6]
            params_json = json.loads(str(paramstring[56]).replace("'", '"'))

            iterator = 0
            list = []
            list.append(event_id)
            for param in params_json:
                key = param
                list.append(str(params_json[key]))
                iterator = iterator + 1

            while iterator <= 9:
                list.append('')
                iterator = iterator + 1

            dict_2 = {"Data": "\n" + str(list).replace("[", "").replace("]", "").replace("'", "")}
            print(dict_2)
            SendToFireHose("event_params", dict_2)

        # Send the finished articles to Kinesis Firehose

        dict_1 = {"Data": line2}
        print(dict_1)
        SendToFireHose("rawdata", dict_1)

        success = "Sent data sucessfully Wahoo!!"
        print(success)


def SendToFireHose(streamName, record):
    response = firehoseClient.put_record(
        DeliveryStreamName=streamName,
        Record=record
    )