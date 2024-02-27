from datetime import timezone
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from config import settings
from stores.models import Store
from stores.serializers import StoreListSerializer
from .models import StoreAccessLog

class RecentStores(APIView):


    permission_classes = [IsAuthenticated] #조회(Get)도 인증되어야함

    def get(self, request):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        user_logs = StoreAccessLog.objects.filter(user=request.user).order_by('-accessed_at').distinct().values_list('store', flat=True)[start:end]
        stores = Store.objects.filter(pk__in=user_logs)
        serializer = StoreListSerializer(
            stores, 
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)
