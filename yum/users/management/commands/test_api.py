from django.core.management.base import BaseCommand
import requests
from dotenv import load_dotenv
import os

class Command(BaseCommand):
    help = "Тест API"

    def handle(self, *args, **kwargs):
        load_dotenv()
        API_KEY = os.getenv("API_KEY")

        address = "Красная площадь, Москва"
        format_address = address.replace(' ', '+')
        print(format_address)


        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={format_address}&key={API_KEY}"
        # params = {"address": format_address, "key": API_KEY}
        # url = f'https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key={API_KEY}'
        response = requests.get(url).json()

        if response["status"] == "OK":
            location = response["results"][0]["geometry"]["location"]
            self.stdout.write(self.style.SUCCESS(f"Координаты: {location['lat']}, {location['lng']}"))
        else:
            self.stdout.write(self.style.ERROR("Ошибка при запросе к API"))
            self.stdout.write(response["error_message"])


