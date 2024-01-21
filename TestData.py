class TestData():
    CHROME_EXECUTABLE_PATH="chromedriver.exe"    
    # BASE_URL = "https://www.mcdonalds.com/de/de-de/restaurant-suche.html/l/berlin"
    RESTAURANT_NAME = "McDonalds"
    COUNTRY = "Germany"
    CITY = "Berlin"
    ADDRESS_URL = "http://www.mapquestapi.com/geocoding/v1/address"
    BASE_URL = f"https://www.mcdonalds.com/de/de-de/restaurant-suche.html/l/{CITY.lower()}"