from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import Wishlist
from stores.models import Store
from .serializers import WishlistSerializer

class Wishlists(APIView):


    permission_classes = [IsAuthenticated] #조회(Get)도 인증되어야함

    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            all_wishlists, 
            many=True,
            context={"request":request},
            )
        return Response(serializer.data)
    
    def post(self, request):

        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(
                user=request.user,
                )
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WishlistDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user) #본인의 Wishlist를 조회하는것이 맞는지까지 조회
        except Wishlist.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(wishlist, context={"request":request})
        return Response(serializer.data)
    
    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_200_OK)
    
    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WishlistToggle(APIView):

    def get_list(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound
        
    def get_store(self, pk):
        try:
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            raise NotFound

    def put(self, request, pk, store_pk):
        wishlist = self.get_list(pk, request.user)
        store = self.get_store(store_pk)
        if wishlist.stores.filter(pk=store.pk).exists():
            wishlist.stores.remove(store) 
        else: 
            wishlist.stores.add(store) 
        return Response(status=HTTP_200_OK)