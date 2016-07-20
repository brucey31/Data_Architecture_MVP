from boto import kinesis
import datetime
import json
import csv
import configparser


config = configparser.ConfigParser()
ini = config.read('conf2.ini')

AWS_ACCESS_KEY_ID = config.get('AWS Credentials', 'key')
AWS_SECRET_ACCESS_KEY = config.get('AWS Credentials', 'secret')

kinesis = kinesis.connect_to_region("eu-west-1", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

print kinesis.list_streams()
print kinesis.describe_stream("rawdata")

initial_uid = 32767376

bruce = "awesome"

while bruce == "awesome":
    with open("Kinesis_Test_Data.csv", 'rb') as source_file:
        contents = csv.reader(source_file, delimiter=',', quotechar='|')

        for event in contents:
            data = dict()

            initial_uid = initial_uid + 1
            data['uid'] = initial_uid
            data['event'] = event[0]
            data['timestamp'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            data['unit'] = event[1]
            data['package'] = event[2]
            data['price'] = event[3]
            data['platform'] = event[4]

            json_data = json.dumps(data, ensure_ascii=False)

            print json_data

            kinesis.put_record("rawdata", json_data, "partitionkey")


    shard_id = 'shardId-000000000000'
    shard_it = kinesis.get_shard_iterator("rawdata", shard_id, "LATEST")["ShardIterator"]
    print shard_it

