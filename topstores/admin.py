from django.contrib import admin
from .models import TopStore

@admin.register(TopStore)
class TopStoreAdmin(admin.ModelAdmin):
    list_display = (
        "updated_at",
        "store",
        "rank",
    )