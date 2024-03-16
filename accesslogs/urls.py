from django.urls import path
from .views import RecentStores

urlpatterns = [
    path("", RecentStores.as_view()),
]