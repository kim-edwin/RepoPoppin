from rest_framework.serializers import ModelSerializer
from stores.serializers import StoreListSerializer
from .models import Wishlist

class WishlistSerializer(ModelSerializer):

    stores = StoreListSerializer(
        many=True, 
        read_only=True,
        )
    

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "stores",
        )