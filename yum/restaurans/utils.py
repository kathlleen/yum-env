import requests
from django.conf import settings
from dotenv import load_dotenv
import os


def get_coordinates(address):
    """Получает широту и долготу по адресу через Google Geocoding API"""
    if not address:
        return None, None

    API_KEY = settings.API_KEY

    format_address = address.replace(' ', '+')
    # print(format_address)

    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={format_address}&key={API_KEY}"

    response = requests.get(url).json()

    if response.get("status") == "OK":
        location = response["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]

    return None, None
