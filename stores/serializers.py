from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Store
from wishlists.models import Wishlist

class StoreDetailSerializer(ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = "__all__"
        #depth = 1

    def get_rating(self, store): #get_필드이름으로 고정시켜야한다. #두번째 인자는 모델이름이 된다.
        return store.rating()
    
    
    def get_is_liked(self, store):
        request = self.context['request']
        return Wishlist.objects.filter(user=request.user, stores__pk=store.pk).exists()
    
class StoreListSerializer(ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = "__all__"
        #depth = 1
    
    def get_rating(self, room):
        return room.rating()
    
    def get_is_owner(self, room):
        request = self.context['request']
        return room.owner == request.user