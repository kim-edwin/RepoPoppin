from datetime import timezone
from django.conf import settings
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from StoreAccessLog.models import StoreAccessLog

from reports.serializers import ReportSerializer
from .models import Store
from .serializers import StoreListSerializer, StoreDetailSerializer
from reviews.serializers import ReviewSerializer

from datetime import datetime, date

# Create your views here.
class Stores(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly] 
    #Get은 권한없이 가능하고, 나머지 메소드들은 authentification이 필요하다.

    def get(self, request):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        visible_stores = Store.objects.filter(is_visible=True).order_by('-id')[start:end]
        serializer = StoreListSerializer(
            visible_stores, 
            many=True,
            context={"request": request},)
        return Response(serializer.data)

class StoreDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly] 

    def get_object(self, pk):
        try:
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        store = self.get_object(pk)
        serializer = StoreDetailSerializer(
            store,
            context={"request": request},
        ) #serializer에 context를 담아 보낼 수 있다. request를 담아 보내면 유용하다.

        if request.user.is_authenticated:
            StoreAccessLog.objects.create(user=request.user, store=store)
        
        return Response(serializer.data)
    
class StoreReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        page = request.query_params.get('page', 1) #url 뒤의 쿼리 파리미터를 가져온다. 자동으로 딕셔너리 형태로 들어온다.
        try:
            page = int(page) #정수형으로 변환
        except ValueError:
            page = 1 #잘못 가져오면 그냥 1페이지 가져오기

        review_size = settings.REVIEW_SIZE
        start = (page - 1) * review_size
        end = start + review_size

        store = self.get_object(pk)
        serializer = ReviewSerializer(
            store.reviews.all().order_by('-created_at')[start:end], #인덱싱이 된다. 이것이 Pagination. 장고는 전체를 가져오지 않고 필요한것만 부른다. QuerySet이라서..
            many=True,
        )
        return Response(serializer.data)
    
    def post(self, request, pk):
        serializer = ReviewSerializer(
            data=request.data
        )
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                store=self.get_object(pk)
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
    
class StoreReports(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            raise NotFound
        
    def post(self, request, pk):
        serializer = ReportSerializer(
            data=request.data
        )
        if serializer.is_valid():
            report = serializer.save(
                user=request.user,
                store=self.get_object(pk)
            )
            serializer = ReportSerializer(report)
            return Response(serializer.data)
        
class StoreSearch(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly] 

    def get(self, request):
        keyword = request.query_params.get("keyword", "")
        upper_addr_name = request.query_params.get("upperAddrName", "")
        middle_addr_name = request.query_params.get("middleAddrName", "")
        search_date = request.query_params.get("searchDate", "")
        is_end = request.query_params.get("isEnd", "True")  # 기본값은 True로 설정
        page = request.query_params.get("page", 1)  # 페이지 번호

        # 페이지 번호 유효성 검사
        try:
            page = int(page)
            if page < 1:
                page = 1
        except ValueError:
            page = 1

        # 페이지 크기 설정
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        # 검색 조건 설정
        query = Q(p_name__icontains=keyword) | Q(p_location__icontains=keyword) | Q(p_hashtag__icontains=keyword)

        if upper_addr_name:
            query &= Q(upperAddrName=upper_addr_name)
        if middle_addr_name:
            query &= Q(middleAddrName=middle_addr_name)
        if search_date:
            search_date = datetime.strptime(search_date, '%Y-%m-%d').date()
            query &= Q(p_startdate__lte=search_date) & Q(p_enddate__gte=search_date)
        if is_end.lower() == "true":  # isEnd가 True인 경우만 종료된 상점 제외
            query &= ~Q(p_startdate=None, p_enddate=None)
            query &= ~(Q(p_enddate__lt=date.today()))

        # 필터링된 상점들을 가져오고 시리얼라이즈
        visible_stores = []
        for store in Store.objects.filter(query).order_by('-p_startdate'):
            if store.p_startdate is None or store.p_enddate is None:
                continue
            visible_stores.append(store)
        visible_stores = visible_stores[start:end]
        serializer = StoreListSerializer(visible_stores, many=True, context={"request": request})

        return Response(serializer.data)