# Import os module for environmental variables
import os
# Import necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values
# Load variables from .env file
load_dotenv()
# Retrieve API Key
API_KEY = os.getenv('API_KEY')

# GeoPy is a Python Client for geocoding web services such as Google's Map Geocoding API
from geopy import geocoders
g = geocoders.GoogleV3(api_key = API_KEY)

def geocode(street, city, state):
    address = street + ', ' + city + ', ' + state

    # Use geocode to retrieve information on the address
    location = g.geocode(address, timeout=10)

    return (location.latitude, location.longitude)
    # print(location.raw)
    # print(location.address)
    