from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from stores.serializers import StoreListSerializer
from topstores.models import TopStore

class TopStores(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        # 모든 TopStore 객체를 가져옵니다.
        top_stores = TopStore.objects.all()

        # TopStore 객체의 store 필드를 가져와 리스트로 만듭니다.
        stores = [top_store.store for top_store in top_stores]

        # StoreListSerializer를 사용하여 stores를 직렬화합니다.
        serializer = StoreListSerializer(
            stores,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)
