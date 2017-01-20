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

        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record['kinesis']['data'])
        print(payload)

        # Break down payload and process
        paramstring = payload.split("\t")
        event_id = paramstring[6]

        for rec in paramstring:
            if 'iglu:com.busuu' in str(rec):
                rec = json.loads(rec)
                schema = rec["data"]["schema"]
                data_to_parse = rec["data"]["data"]
                print("Parsing data from " + str(schema))

                if schema == "iglu:com.busuu/standard_event/jsonschema/1-0-0":
                    print(data_to_parse)

                    event = data_to_parse["event"]
                    interface_language = data_to_parse["interface_language"]
                    platform = data_to_parse["platform"]
                    app_id = data_to_parse["app_id"]
                    version = data_to_parse["version"]
                    try:
                        language_learnt = data_to_parse["language_learnt"]
                    except Exception as e:
                        language_learnt = ''
                    try:
                        operating_system_version = data_to_parse["operating_system_version"]
                    except Exception as e:
                        operating_system_version = ''
                    try:
                        idfa = data_to_parse["idfa"]
                    except Exception as e:
                        idfa = ''
                    try:
                        role = data_to_parse["role"]
                    except Exception as e:
                        role = ''

                    params = data_to_parse["params"]
                    if params != '':
                        print("Found params")
                        params = json.loads(str(params).replace("'", "\"").replace("u", ''))
                        listo = []
                        listo.append(event_id)
                        iterator = 0
                        for param in params:
                            listo.append(str(params[param]))
                            iterator = iterator + 1

                        while iterator <= 9:
                            listo.append('')
                            iterator = iterator + 1

                        dict_2 = {"Data": "\n" + str(listo).replace("[", "").replace("]", "").replace("'", "")}
                        print("Data going to snowplow_params = " + str(dict_2))
                        SendToFireHose("event_params", dict_2)


        if schema == "iglu:com.busuu/standard_event/jsonschema/1-0-0":
            iterator = 0

            for item in paramstring:
                if iterator == 52:
                    paramstring[iterator] = event
                if iterator == 53:
                    paramstring[iterator] = interface_language
                if iterator == 54:
                    paramstring[iterator] = language_learnt
                if iterator == 55:
                    paramstring[iterator] = app_id
                if iterator == 56:
                    paramstring[iterator] = operating_system_version
                if iterator == 57:
                    paramstring[iterator] = role
                if iterator == 58:
                    paramstring[iterator] = idfa
                if iterator == 60:
                    paramstring[iterator] = platform
                if iterator == 61:
                    paramstring[iterator] = version
                iterator = iterator + 1

        # Send the finished articles to Kinesis Firehose
        dict_1 = {"Data": "\nBusuu" + str(paramstring).replace(", u'", ",'").replace("[", "").replace("]", "").replace("'", "").replace(" ", "")}
        print("Data going to snowplow_events = " + str(dict_1))
        SendToFireHose("rawdata", dict_1)

        success = "Sent data sucessfully Wahoo!!"
        print(success)


def SendToFireHose(streamName, record):
    response = firehoseClient.put_record(
        DeliveryStreamName=streamName,
        Record=record
    )
