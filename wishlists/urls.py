from django.urls import path
from .views import WishlistDetail, WishlistToggle #Wishlists, 

urlpatterns = [
    # path("", Wishlists.as_view()),
    path("", WishlistDetail.as_view()),
    # path("<int:pk>", WishlistDetail.as_view()),
    path("stores/<int:store_pk>", WishlistToggle.as_view()),
]