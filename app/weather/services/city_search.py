from typing import Any

import requests
from django.conf import settings
from django.db.models import Count
from django.http import HttpRequest

from weather.models import CitySearch


class CityAutocompleteService:
    def __init__(self, request: HttpRequest):
        self.query = request.GET.get("query", "").lower()
        self.API_KEY = settings.OPENWEATHERMAP_API_KEY

    def get_results(self) -> list[dict[str, Any]]:
        if not self.query:
            return []

        exclude_words = ['district', 'county', 'region', 'okrug', 'район', 'округ', 'область', 'край']
        results = []
        for item in self._search_city():
            local_names = item.get("local_names", {})
            city_name_ru = local_names.get("ru")
            city_name = city_name_ru or item.get("name", "")

            if not city_name.lower().startswith(self.query):
                continue
            if any(word in city_name.lower() for word in exclude_words):
                continue

            name_parts = [city_name]
            if state := item.get("state"):
                name_parts.append(state)
            if country := item.get("country"):
                name_parts.append(country)

            results.append({
                "name": ", ".join(name_parts),
                "lat": item.get("lat"),
                "lon": item.get("lon"),
            })

        return results

    def _search_city(self) -> list[dict[str, Any]]:
        url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {"q": self.query, "limit": 5, "appid": self.API_KEY}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return []
        return response.json()


class CityStatsService:
    def get_stats(self) -> list[dict[str, Any]]:
        return (
            CitySearch.objects
            .values("city")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

    def get_stats_for_session(self, request: HttpRequest) -> list[dict[str, Any]]:
        searched_cities = request.session.get('searched_cities', [])
        if not searched_cities:
            return []
        return (
            CitySearch.objects
            .filter(city__in=searched_cities)
            .values("city")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
