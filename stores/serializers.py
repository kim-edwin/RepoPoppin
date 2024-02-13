from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Store
from wishlists.models import Wishlist

class StoreDetailSerializer(ModelSerializer):

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = "__all__"
        #depth = 1

    def get_rating(self, store): #get_필드이름으로 고정시켜야한다. #두번째 인자는 모델이름이 된다.
        return store.rating()
    
    
class StoreListSerializer(ModelSerializer):
    rating = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = (
            "p_name",
            "p_startdate",
            "p_enddate",
            "img_url",
            "p_location",
            "p_hashtag",
            "rating",
            "status",
        )
        #depth = 1
    
    def get_rating(self, store):
        return store.rating()
    
    def get_status(self, store):
        return store.status()
    