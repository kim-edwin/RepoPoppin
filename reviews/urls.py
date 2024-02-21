from django.urls import path, include
from .views import ReviewDetail

urlpatterns = [
    path("<int:pk>", ReviewDetail.as_view()),
]