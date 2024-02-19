from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = (
                "p_name",
                "p_startdate",
                "p_enddate",
                "p_location",
                "is_visible",
                    )

    list_filter = (
        "is_visible",
        "p_startdate",
        "p_enddate",
    )

    list_editable = (
        "is_visible",
    )

    search_fields = (
        "name",
        "is_visible",
    )

    def make_visible(self, request, queryset):
        queryset.update(is_visible=True)

    def make_hidden(self, request, queryset):
        queryset.update(is_visible=False)

    make_visible.short_description = "선택한 항목을 표시로 변경"
    make_hidden.short_description = "선택한 항목을 숨김으로 변경"

    actions = [make_visible, make_hidden]