from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "hash_tags",
        "rating",
        "poi_address",
        "is_visible",
    )

    list_filter = (
        "is_visible",
    )

    # def total_amenities(self, room):
    #     return room.amenities.count()

    search_fields = (
        "name",
        "is_visible",
    )