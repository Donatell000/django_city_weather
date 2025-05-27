from django.urls import path

from .views import WeatherView, CityAutocompleteView, StatsView, GlobalStatsView


urlpatterns = [
    path("api/cities/", CityAutocompleteView.as_view(), name="city_autocomplete"),
    path("stats/", StatsView.as_view(), name="city_stats_api"),
    path("stats/global/", GlobalStatsView.as_view(), name="global_stats"),
    path("weather/", WeatherView.as_view(), name="home"),
]
