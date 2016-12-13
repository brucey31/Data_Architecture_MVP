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

        # TSV to CSV
        # jsons = re.sub("{", '"{', payload)
        # jsons2 = re.sub("}", '}"', jsons)
        line = re.sub("\t", ",", payload)
        # line2 = re.sub("\"\"", "\"", line)
        line2 = re.sub("Busuu", "\nBusuu", line)
        print(line)
        print("Raw data = " + str(line2))

        # Break down params json 58
        paramstring = payload.split("\t")
        event_id = paramstring[6]

        if paramstring[58] != "":
            print("Found params")
            event_params = json.loads(paramstring[58])
            event_params = event_params["data"]["data"]

            uid = event_params["uid"]
            interface_language = event_params["interface_language"]
            language_learnt = event_params["language_learnt"]
            app_id = event_params["app_id"]
            environment = event_params["environment"]
            platform = event_params["platform"]
            version = event_params["version"]
            user_agent = event_params["user_agent"]
            event = event_params["event"]
            params = event_params["params"]

            try:
                idfa = event_params["idfa"]
            except:
                idfa = ''
            try:
                data_status = event_params["data_status"]
            except:
                data_status = ''
            try:
                role = event_params["role"]
            except:
                role = ''

            params = json.loads(params.replace("'", "\""))

            list = []
            list.append(event_id)
            iterator = 0
            for param in params:
                list.append(str(params[param]))
                iterator = iterator + 1
                # event_id = paramstring[6]
                # params_json = json.loads(str(paramstring[56]).replace("'", '"'))

            while iterator <= 9:
                list.append('')
                iterator = iterator + 1

            dict_2 = {"Data": "\n" + str(list).replace("[", "").replace("]", "").replace("'", "")}
            print("Data going to snowplow_params = " + str(dict_2))
            SendToFireHose("event_params", dict_2)
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
                    paramstring[iterator] = user_agent
                if iterator == 57:
                    paramstring[iterator] = role
                if iterator == 58:
                    paramstring[iterator] = idfa
                if iterator == 59:
                    paramstring[iterator] = environment
                if iterator == 60:
                    paramstring[iterator] = platform
                if iterator == 61:
                    paramstring[iterator] = version
                iterator = iterator + 1



        # Send the finished articles to Kinesis Firehose
        dict_1 = {"Data": "\n" + str(paramstring).replace(", u'",",'").replace("[", "").replace("]", "").replace("'", "").replace(" ", "")}
        print("Data going to snowplow_events = " + str(dict_1))
        SendToFireHose("rawdata", dict_1)

        success = "Sent data sucessfully Wahoo!!"
        print(success)


def SendToFireHose(streamName, record):
    response = firehoseClient.put_record(
        DeliveryStreamName=streamName,
        Record=record
    )