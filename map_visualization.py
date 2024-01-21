# import required libraries 
import pandas as pd
import folium
from folium import FeatureGroup
from folium.plugins import MarkerCluster
import sys
import json
import os
from kafka import KafkaConsumer

from dotenv import load_dotenv
load_dotenv()

KAFKA_MAP_TOPIC_WITH_LAT_LONG = os.environ['KAFKA_MAP_TOPIC_WITH_LAT_LONG']

consumer = KafkaConsumer(
    KAFKA_MAP_TOPIC_WITH_LAT_LONG, 
    bootstrap_servers="localhost:29093",
    auto_offset_reset = "earliest"
)

class Visualization():
    def __init__(self):
        #Create the base Map
        self.marker = folium.Map(location=[48.86762,2.3624], tiles='OpenStreetMap', zoom_start=5)

        #Create the markers
        self.markerCluster = MarkerCluster().add_to(self.marker)

    def visualize(self):
        for msg in consumer:
            consumed_message = json.loads(msg.value)
            print(consumed_message)
            lat = consumed_message.get("lat")
            lng = consumed_message.get("lng")
            restaurant = consumed_message.get("restaurant")

            popup = restaurant +'<br>' + str(consumed_message.get("street")) +'<br>' + str(consumed_message.get("zip"))

            if restaurant == 'McDonalds':
                color = 'red'
            else:
                color = 'green'

            folium.Marker(location=[lat, lng],popup=restaurant, icon=folium.Icon(color=color)).add_to(self.markerCluster)

            self.marker.save("index.html")


if __name__ == "__main__":
    print(' [*] Waiting for messages. To exit press CTRL+C')
    try:
        vis = Visualization()
        vis.visualize()

    except Exception as e:
        print(e) 

    except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

