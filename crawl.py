from selenium import webdriver
from bs4 import BeautifulSoup as BS
import time
import csv
import json

from TestData import TestData 

from dotenv import load_dotenv
load_dotenv()
from kafka import KafkaProducer
import sys
import os

#Create a Chrome driver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver=webdriver.Chrome()

KAFKA_MAP_TOPIC = os.environ['KAFKA_MAP_TOPIC']
SLEEP_TIME = int(os.environ['SLEEP_TIME'])

class Crawler():
    def __init__(self, driver, url, restaurantName, country, city):
        self.driver=driver
        self.restaurantName = restaurantName
        self.country = country
        self.city = city
        self.driver.get(url)   
        #give time for all javascripts to be finished running
        time.sleep(10)
        self.page = self.driver.page_source
        self.soup = BS(self.page, "html.parser")
    
    def search(self, element='ul', query='ubsf_sitemap-list'):
        self.content = self.soup.find(element, class_=query)
        return self.content

    def getRestaurantList(self, element='div', query='ubsf_sitemap-location-address'):
        self.restaurantList = self.search().find_all(element, class_=query)
        return self.restaurantList
    
    def tearDown(self):
        # To do the cleanup after test has executed.
        self.driver.close()
        self.driver.quit()

    def createDataset(self, restaurant):
        dict_restaurants = {}
        street = restaurant.text.split(",")[0]
        zipCode = restaurant.text.split(",")[1][1:6]
        dict_restaurants["restaurant"] = self.restaurantName
        dict_restaurants["street"] = street
        dict_restaurants["zip"] = zipCode
        dict_restaurants["city"] = self.city
        dict_restaurants["country"] = self.country
        return dict_restaurants
    
    # function to add to JSON
    def write_json(self, new_data, filename='data.json'):
        with open(filename,'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data["details"].append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file)
    
    def my_crawler(self):
        restaurant_details = []
        for restaurant in self.getRestaurantList():
            result = self.createDataset(restaurant)
            restaurant_details.append(result)
        return json.dumps(restaurant_details)




def json_serializer(data):
    return json.dumps(data).encode("utf-8")

producer = KafkaProducer(bootstrap_servers = "localhost:9092",
                         value_serializer=json_serializer)

if __name__ == "__main__":
    try:
        crawl = Crawler(driver=driver,
                        url=TestData.BASE_URL,
                        restaurantName=TestData.RESTAURANT_NAME, 
                        country=TestData.COUNTRY, 
                        city=TestData.CITY)
        restaurant_details = crawl.my_crawler()
        crawl.tearDown() 
        restaurant_details = json.loads(restaurant_details)
        print("[*] Waiting for messages.  Sending to Kafka consumer to GET GeoLocation, To exit press CTRL+C")
        for restaurant_detail in restaurant_details:
            producer.send(KAFKA_MAP_TOPIC, restaurant_detail)
            time.sleep(SLEEP_TIME)

    except Exception as e:
        print(e) 

    except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

