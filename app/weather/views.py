from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from .services.city_search import CityAutocompleteService, CityStatsService
from .services.weather import WeatherService


class WeatherView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        service = WeatherService(request)
        context = service.get_context()
        return render(request, "weather.html", context)

    def post(self, request: HttpRequest) -> HttpResponse:
        service = WeatherService(request)
        context, response = service.handle_post()
        return response or render(request, "weather.html", context)


class CityAutocompleteView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        service = CityAutocompleteService(request)
        return JsonResponse(service.get_results(), safe=False)


class StatsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        stats = CityStatsService().get_stats_for_session(request)
        return render(request, "stats.html", {"stats": stats, "title": "Ваша статистика"})


class GlobalStatsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        stats = CityStatsService().get_stats()
        return render(request, "stats.html", {"stats": stats, "title": "Общая статистика"})
