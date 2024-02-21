from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from reviews.serializers import ReviewSerializer
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Review

class ReviewDetail(APIView):

    permission_classes = [IsAuthenticated] 

    def get_object(self, pk, user):
        try:
            return Review.objects.get(pk=pk, user=user) #본인의 Wishlist를 조회하는것이 맞는지까지 조회
        except Review.DoesNotExist:
            raise NotFound
    
    def delete(self, request, pk):
        Review = self.get_object(pk, request.user)
        Review.delete()
        return Response(status=HTTP_200_OK)