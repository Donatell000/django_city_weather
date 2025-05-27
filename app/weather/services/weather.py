import urllib.parse
from typing import Any

import requests
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from weather.forms import CityForm
from weather.models import CitySearch


class WeatherService:
    def __init__(self, request: HttpRequest):
        self.request = request
        self.API_KEY = settings.OPENWEATHERMAP_API_KEY
        self.city = ""
        self.weather = None
        self.error = None

    def get_context(self) -> dict[str, Any]:
        form = CityForm()
        last_city_encoded = self.request.COOKIES.get("last_city")
        last_city = urllib.parse.unquote(last_city_encoded) if last_city_encoded else None

        return {
            "form": form,
            "weather": None,
            "error": None,
            "last_city": last_city,
            "show_last_city_block": True,
        }

    def handle_post(self) -> tuple[dict[str, Any], HttpResponse | None]:
        form = CityForm(self.request.POST)
        last_city_encoded = self.request.COOKIES.get("last_city")
        last_city = urllib.parse.unquote(last_city_encoded) if last_city_encoded else None

        if form.is_valid():
            self.city = form.cleaned_data["city"]
            self.weather = self._get_weather()

            if self.weather is None:
                self.error = "Не удалось получить погоду"
            else:
                searched_cities = self.request.session.get('searched_cities', [])
                if self.city not in searched_cities:
                    searched_cities.append(self.city)
                    self.request.session['searched_cities'] = searched_cities

                response = render(self.request, "weather.html", {
                    "form": form,
                    "weather": self.weather,
                    "error": None,
                    "last_city": last_city,
                    "show_last_city_block": False,
                })
                response.set_cookie("last_city", urllib.parse.quote(self.city), max_age=30 * 24 * 60 * 60,
                                    httponly=True)
                CitySearch.objects.create(
                    city=self.city,
                    ip_address=self.request.META.get("REMOTE_ADDR", "0.0.0.0")
                )
                return {}, response

        return {
            "form": form,
            "weather": self.weather,
            "error": self.error,
            "last_city": last_city,
            "show_last_city_block": True,
        }, None

    def _get_weather(self) -> dict[str, Any] | None:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": self.city,
            "appid": self.API_KEY,
            "units": "metric",
            "lang": "ru",
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return None
        return response.json()
