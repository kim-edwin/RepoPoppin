from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = (
        "status",
        "name",
        "start_date",
        "end_date",
        "img_url",
        "hash_tags",
        "poi_address",
        "is_visible",
    )

    list_filter = (
        "is_visible",
    )

    list_editable = (
        "is_visible",
    )



    search_fields = (
        "name",
        "is_visible",
    )