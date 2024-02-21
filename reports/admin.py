from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "get_store_name",
        "payload",
    )

    def get_store_name(self, obj):
        return obj.store.p_name if obj.store else "None"

    get_store_name.short_description = "Store Name"