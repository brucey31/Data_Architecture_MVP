from snowplow_tracker import Subject, Tracker, Emitter, SelfDescribingJson
import socket
import csv
import datetime
import random

app_id = 'Busuu'
# e = Emitter("10.0.52.22", port=8080)
e = Emitter("events.busuu.com", port=80)
t = Tracker(e, app_id=app_id, encode_base64=True)

ip = socket.gethostbyname(socket.gethostname())

bruce = "awesome"
while bruce == "awesome":
    with open('Kinesis_Test_Data2.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            event_name = row[0]
            timestamp = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds())

            # if event_name == 'page_view':
            #     web_page = row[1]
            #     page_name = row[2]
            #     referral_string = row[3]
            #     b_source = row[8]
            #     b_campaign = row[5]
            #     platform = row[4]
            #     b_group = row[6]
            #     b_term = row[7]
            #
            #     # custom_context = [{"b_source": b_source, "b_campaign": b_campaign, "b_term": b_term, "b_group": b_group}]
            #     custom_context = SelfDescribingJson("iglu:com.busuu/web_attribution/jsonschema/2-1-1", {"b_source": b_source, "b_campaign": b_campaign, "b_term": b_term, "b_group": b_group})
            #
            #     if b_source != "" and b_source:
            #         t.track_page_view(web_page, page_name, referral_string, context=[custom_context])
            #     if referral_string != "" and referral_string:
            #         t.track_page_view(web_page, page_name, referral_string)
            #     else:
            #         t.track_page_view(web_page, page_name)
            #
            #
            # if event_name == "purchased" or event_name == 'purchase_complete':
            #     s = Subject()
            #
            #     unit_id = row[1]
            #     package = str(row[2]).replace("['", "").replace("']", "")
            #     price = float(row[3])
            #     platform = row[4]
            #     uid = row[5]
            #     currency = row[6]
            #     email = row[9]
            #
            #     t.subject.set_platform(platform).set_user_id(uid).set_lang("enc").set_ip_address(ip)
            #
            #     items = [{"sku": "made_up_SKU", "price": price, "quantity": 1, "name": str(package)}]
            #     t.track_ecommerce_transaction("A-0000001234", price, email, None, None , None , None , None , currency, items , None , timestamp)
            #

            interface_language = row[1]
            language_learnt = row[2]
            b_source = row[3]
            b_campaign = row[8]
            uid = row[5]
            platform = row[4]
            b_term = row[6]
            b_group = row[7]
            email = row[9]

            custom_context = str(
                {"source": b_source, "campaign": b_campaign, "term": b_term, "group": b_group, "email": email})

            # Set params for specific User
            s = Subject()
            t.subject.set_platform(platform).set_user_id(uid).set_lang("enc").set_ip_address(ip)

            # Send it to emitter
            # t.track_struct_event(event_name, interface_language, language_learnt, custom_context, None, None, timestamp)

            schema = "iglu:com.busuu/standard_event/jsonschema/1-0-0"
            event = SelfDescribingJson(schema=schema,
                                       data={
                                           "event": event_name,
                                           "uid": uid,
                                           "language_learnt": language_learnt,
                                           "interface_language": interface_language,
                                           "params": custom_context,
                                           "platform": platform,
                                           "app_id": "app_id_1",
                                           "version": "1.563_bruce",
                                           "environment": "brucetopia",
                                           "user_agent": "007_licence_to_kill",
                                           "idfa": "23456yhvfrtyujb",
                                           "data_status": "%s" % random.choice(["offline", "wi-fi", "cellular"]),
                                           "role": "%s" % random.choice(["premium", "pro", "free"])
                                       })

            t.track_unstruct_event(event)
