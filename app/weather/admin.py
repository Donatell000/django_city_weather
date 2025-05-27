from django.contrib import admin

from .models import CitySearch


@admin.register(CitySearch)
class CitySearchAdmin(admin.ModelAdmin):
    list_display = ("city", "ip_address")
    list_filter = ("city",)
    search_fields = ("city", "ip_address")
