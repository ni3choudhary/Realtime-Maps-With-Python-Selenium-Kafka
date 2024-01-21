# import required libraries 
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

import requests

from TestData import TestData
import json
pd.set_option('display.max_rows', None)
from kafka import KafkaConsumer, KafkaProducer
import sys

API_KEY = os.environ['API_KEY']
KAFKA_MAP_TOPIC = os.environ['KAFKA_MAP_TOPIC']
KAFKA_MAP_TOPIC_WITH_LAT_LONG = os.environ['KAFKA_MAP_TOPIC_WITH_LAT_LONG']



consumer = KafkaConsumer(
    KAFKA_MAP_TOPIC, 
    bootstrap_servers="localhost:29093",
    auto_offset_reset = "earliest"
)

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

producer = KafkaProducer(bootstrap_servers="localhost:29093",
                         value_serializer=json_serializer)

class GetGeo():

    def __init__(self, url = None, api_key = API_KEY):
        self.api_key = api_key
        self.url = url

    def parameters(self, address = None):
        params = {
            "key": self.api_key,
            "location": address
        }

        return params

    def getLatLong(self):
        for msg in consumer:
            consumed_message = json.loads(msg.value)
            api_address = str(consumed_message.get("street")) \
                            + ','+str(consumed_message.get("zip")) \
                            +','+str(consumed_message.get("city")) \
                            +','+str(consumed_message.get("country"))

            parameters = self.parameters(api_address)
            response = requests.get(self.url, params=parameters)
            data = response.text
            dataJ = json.loads(data)['results']
            lat = (dataJ[0]['locations'][0]['latLng']['lat'])
            lng = (dataJ[0]['locations'][0]['latLng']['lng'])

            consumed_message['lat'] =  lat
            consumed_message['lng'] =  lng
            print(consumed_message)
            print('--------------------------------Sending Data...........................................')
            producer.send(KAFKA_MAP_TOPIC_WITH_LAT_LONG, consumed_message)



if __name__ == "__main__":
    print(' [*] Waiting for messages. To exit press CTRL+C')
    try:
        getGeo = GetGeo(url=TestData.ADDRESS_URL,
                        api_key = API_KEY
                        )
        while True:
            getGeo.getLatLong()

    except Exception as e:
        print(e) 

    except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)