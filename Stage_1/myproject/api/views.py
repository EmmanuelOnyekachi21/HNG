from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import requests

# Create your views here.
class HandleViews(View):
    """
    Using Class Based Views to handle GET requests.
    """
    def get(self, request):
        """
        The get method
        """
        # Get visitor's name from Query Parameters
        visitor = request.GET.get('visitor_name', 'Visitor')

        # Get the IP address of the requester
        #client_ip = request.META.get('REMOTE_ADDR')
        client_ip = '8.8.8.8'

        # Fetch location Data using IPInfo API
        ipinfoAccessToken = 'd96d756a8e799e'
        response = requests.get(
                f'https://ipinfo.io/{client_ip}'
                f'/json?token={ipinfoAccessToken}')
        location_data = response.json()

        city = location_data.get('city', 'Unknown location')

        # Fetch the weather Data using OpenWeather API
        weatherApiKey = 'a78550286f566ddbd01f1be56c0b9385'
        weather_response = requests.get(
                f'http://api.openweathermap.org/data/2.5/weather?q='
                f'{city}&appid={weatherApiKey}&units=metric')
        weatherData = weather_response.json()

        if 'main' in weatherData:
            temperature = weatherData['main']['temp']
            greeting = (f"Hello, {visitor}!, the temperature "
            f"is {temperature} degrees Celsius in {city}"
                        )
        else:
            # Handle the case where 'main' is not in the response
            temperature = "unknown"
            greeting = (
                    f"Hello, {visitor}!. unable to fetch temperaature"
                    f" for {city}. Please check city name or API key."
                    )
        return JsonResponse({
            "client_ip": client_ip,
            "location": city,
            "greeting": greeting
        })
