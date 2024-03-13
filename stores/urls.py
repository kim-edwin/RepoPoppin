from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.Stores.as_view()),
    path("search", views.StoreSearch.as_view()),
    path("info", views.StoreInfo.as_view()),
    path("<int:pk>", views.StoreDetail.as_view()),
    path("<int:pk>/reviews", views.StoreReviews.as_view()),
    path("<int:pk>/reports", views.StoreReports.as_view()),
]