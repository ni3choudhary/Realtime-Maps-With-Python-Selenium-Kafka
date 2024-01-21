## Realtime-Maps-With-Python-Selenium-Kafka

This repository contains a set of Python scripts for a web scraping and data visualization project that retrieves McDonald's restaurant locations in a specific city for the GERMANY, extracts their address details, obtains geolocation information and visualizes the locations on a map.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)

## Prerequisites

Before running the script, ensure you have the following prerequisites installed:

- Python 3.x Installed.
- Required Python packages listed in requirements.txt (install using pip install -r requirements.txt)

## Getting Started

To create a project from scratch use following steps -

1. Clone the repository to your local machine.
    ```bash
    git clone https://github.com/your-username/realtime-maps-with-python-selenium-kafka.git
    cd Realtime-Maps-With-Python-Selenium-Kafka
    ```

2. To run Zookeeper and kafka services, run the Docker Compose configuration provided, you can follow these steps:

    i.   Save the given `docker-compose.yml` file to a directory of your choice.
    ii.  Open a terminal or command prompt, navigate to the directory where the `docker-compose.yml` file is located.
    iii. Run the following command to start the services:
    ```bash
    docker-compose up -d
    ```
    The `-d` flag is used to run the containers in the background.

    iv.  Wait for the containers to be downloaded (if not already available) and started. You can check the status of the running containers using:
    ```bash
    docker-compose ps
    ```

    You should see the status of the zookeeper and kafka containers as "Up."

    Your Kafka and Zookeeper services should now be running. The configuration exposes Zookeeper on port 22182 and Kafka on port 29093. You can use these ports to connect to your Kafka instance. Change the ports according to your requirements.

    To stop the services when you are done, you can run:
    ```bash
    docker-compose down
    ```


3. Create Python Virtual Environment using below command (The recommended python version is 3.11.0).
    ```bash
    python -m venv venv
                OR
    conda activate -p venv python==3.11
    ```

4. Activate Virtual Environment

    ```bash
    .venv/bin/activate 
            OR
    .\venv\Scripts\activate
            OR
    source ./venv/Scripts/activate
    ```

- if you have used conda to create the virtual environment, use the following command to activate the virtual environment.

    ```bash
    conda activate venv
    ```

5. Install dependencies using below command
    ```bash
    pip install -r requirements.txt
    ```

6. Download the appropriate ChromeDriver executable for your Chrome version and set the **CHROME_EXECUTABLE_PATH** in `TestData.py` accordingly. I am using chrome version - 114, I was encoutering some problem in recent chrome version (120) thats why I downgraded the chrome browser.

7. Set the environment variable in `.env` file.

    - API_KEY = <your_geocoding_api_key>
    - SLEEP_TIME = "4"
    - KAFKA_MAP_TOPIC = "maps_details"
    - KAFKA_MAP_TOPIC_WITH_LAT_LONG = "maps_details_with_lat_long"

8. This module `TestData.py` defines a TestData class with constants representing test data, such as Chrome executable path, base URL, restaurant name, country, city and address URL.

9. To scrape McDonald's restaurant details from a specific city's. Go inside the **Realtime-Maps-With-Python-Selenium-Kafka** directory and run the script.
    ```bash
    python crawl.py
    ```

    The Script used for the following task - 
    
    i.   This script uses Selenium and BeautifulSoup to scrape McDonald's restaurant details from a specific city's.

    ii.  It creates a Crawler class with methods for searching, retrieving restaurant lists, tearing down the Selenium driver, creating datasets, and writing data to a JSON file.

    iii. The script utilizes Kafka to send the restaurant details to another script for geolocation processing.

10. To retrieve lat and log for the scraped data. Go inside the **Realtime-Maps-With-Python-Selenium-Kafka** directory and run the script. 
    ```bash
    python get_geolocation.py
    ```

    The Script used for the following task - 

    - This script consumes restaurant details from Kafka, constructs an API address, sends a request to a geocoding API, retrieves latitude and longitude information and then sends the enriched data back to Kafka for visualization.

11. To Visualize the locations on a map. Go inside the **Realtime-Maps-With-Python-Selenium-Kafka** directory and run the script.
    ```bash
    python map_visualization.py
    ```

    - This script consumes geolocated restaurant details from Kafka and uses Folium to visualize them on an interactive map. The markers are color-coded based on the restaurant name. You can visualize the results on newly created `index.html`.

`Note`:

- Make sure you have Kafka running, If not, please run the docker-compose file.
- The scripts are designed to work together and running them out of order may result in unexpected behavior.
- Adjust sleep times, Kafka topics and other configurations based on your requirements.