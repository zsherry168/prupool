import os
import googlemaps
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API Key from environment variables
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
print(f"Loaded API Key: {API_KEY}")  # Debug print

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=API_KEY)

def calculate_distance(home_address, work_building_address):
    print(f"Calculating distance from {home_address} to {work_building_address}")  # Debug print
    # Request distance matrix
    result = gmaps.distance_matrix(origins=[home_address], destinations=[work_building_address], mode="driving")

    # Extract the distance and duration
    distance = result['rows'][0]['elements'][0]['distance']['text']
    duration = result['rows'][0]['elements'][0]['duration']['text']

    return distance, duration