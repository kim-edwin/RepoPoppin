from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = (
"p_name",
"p_startdate",
"p_enddate",
"img_url",
"p_location",
"p_hashtag",
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