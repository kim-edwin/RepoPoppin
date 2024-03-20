from datetime import timezone
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied

from accesslogs.models import AccessLog
from reports.serializers import ReportSerializer
from reviews.models import Review
from .models import Store
from .serializers import StoreListSerializer, StoreDetailSerializer, StoreNearSerializer
from reviews.serializers import ReviewSerializer

from datetime import datetime, date
from geopy.distance import geodesic
import numpy as np
import pandas as pd
from keras.models import load_model
from Recommend.models import RecommenderNet

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

        today = date.today()

        visible_stores = Store.objects.filter(is_visible=True, p_enddate__gte=today).order_by('-id')[start:end]
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
            AccessLog.objects.create(user=request.user, store=store)
        
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
    
class StoreInfo(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly] 

    def get(self, request):
        news_ids_param = request.query_params.get("newsId", "")
        news_ids = [x.strip() for x in news_ids_param.split(",") if x.strip()]
        
        stores = []
        for news_id in news_ids:
            try:
                store = Store.objects.get(news_id=news_id)
                serializer = StoreDetailSerializer(store, context={"request": request})
                stores.append(serializer.data)
            except Store.DoesNotExist:
                # Handle the case where the store with given newsId does not exist
                pass
        
        return Response(stores)
    
class StoreSim(APIView):

    def get_object(self, pk):
        try:
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        chucheon = self.get_object(pk).p_chucheon
        chucheon_list = chucheon.split(',')
        stores = []
        for news_id in chucheon_list:
            try:
                store = Store.objects.get(news_id=news_id)
                serializer = StoreListSerializer(store, context={"request": request})
                stores.append(serializer.data)
            except Store.DoesNotExist:
                pass

        return Response(stores)

class StoreNear(APIView):
    def get(self, request):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        # 사용자의 현재 위치
        user_location = (float(latitude), float(longitude))

        # 5km 반경 내의 상점을 조회
        near_stores = Store.objects.filter(
            p_startdate__lte=timezone.now(),
            p_enddate__gte=timezone.now(),
            is_visible=True
        )

        # 거리를 계산하여 상점들을 정렬
        near_stores = sorted(near_stores, key=lambda store: geodesic(user_location, (float(store.frontLat), float(store.frontLon))).kilometers)

        # 가장 가까운 5개의 상점만 선택
        near_stores = near_stores[:5]

        # 거리 정보를 Serializer에 전달하기 위해 context에 사용자 위치 추가
        serializer = StoreNearSerializer(near_stores, many=True, context={"request": request, "user_location": user_location})
        return Response(serializer.data)

class StoreComming(APIView):
    def get(self, request):
        now = timezone.now()
        
        comming_stores = Store.objects.filter(
            p_startdate__gt=now,
            is_visible=True
        ).order_by('p_startdate')[:5]

        serializer = StoreListSerializer(
            comming_stores,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)
    
class NewsRecommender:
    def __init__(self, model_path, request):
        self.model_path = model_path
        self.model = None
        self.news_new2news_encoded = None
        self.user = request.user.pk
    
    def load_data(self):

        
        stores = Store.objects.all().values('id', 'news_id', 'p_enddate')
        stores_store_df = pd.DataFrame(stores)

        # reviews_review_df = pd.read_sql_query(query2, self.connection)
        reviews = Review.objects.all().values('store', 'user', 'rating')
        reviews_review_df = pd.DataFrame(reviews)
        
        chucheon_df = pd.merge(reviews_review_df, stores_store_df, left_on='store', right_on='id')

        self.new_chucheon_df = chucheon_df[['news_id', 'user', 'rating']]
        self.stores_store_df = stores_store_df

        user_ids = reviews_review_df["user"].unique().tolist()
        news_ids = stores_store_df["news_id"].unique().tolist()

        self.user2user_encoded = {x: i for i, x in enumerate(user_ids)}  # 사용자 ID를 인덱스로 매핑하는 딕셔너리
        self.userencoded2user = {x: i for i, x in enumerate(user_ids)}  #  ID를 인덱스로 매핑하는 딕셔너리

        self.news2news_encoded = {x: i for i, x in enumerate(news_ids)}  # 뉴스 ID를 인덱스로 매핑하는 딕셔너리
        self.news_encoded2news  = {x: i for i, x in enumerate(news_ids)}  # 뉴스 ID를 인덱스로 매핑하는 딕셔너리
        
    def load_model(self):
        self.model = load_model(self.model_path, custom_objects={'RecommenderNet': RecommenderNet})
    
    def recommend_news(self):
        news_watched_by_user = self.new_chucheon_df[self.new_chucheon_df.user == self.user]
        news_not_watched = self.stores_store_df[
            (~self.stores_store_df["news_id"].isin(news_watched_by_user.news_id.values)) & 
            (self.stores_store_df["p_enddate"] > date.today())]["news_id"]
        
        news_not_watched = list(set(news_not_watched).intersection(set(self.news2news_encoded.keys())))
        news_not_watched = [[self.news2news_encoded.get(x)] for x in news_not_watched]
        
        user_encoder = self.user2user_encoded.get(self.user)
        user_news_array = np.hstack(([[user_encoder]] * len(news_not_watched), news_not_watched))
        ratings = self.model.predict(user_news_array).flatten()
        top_ratings_indices = ratings.argsort()[-5:][::-1]
        
        selected_news_indices = [news_not_watched[i] for i in top_ratings_indices]
        self.news_new2news_encoded = {value: key for key, value in self.news_encoded2news.items()}
        recommended_news_ids = [self.news_new2news_encoded[index[0]] for index in selected_news_indices]
        return recommended_news_ids
    
class StoreRecommend(APIView):
    
    def get(self, request):
        recommender = NewsRecommender(
            model_path="./Recommend/recommender_model.keras",
            request=request
        )
        recommender.load_data()
        recommender.load_model()
        recommended_news_ids = recommender.recommend_news()

        stores = []

        for id in recommended_news_ids:
            try:
                store = Store.objects.get(news_id=id)
                serializer = StoreListSerializer(store, context={"request": request})
                stores.append(serializer.data)
            except Store.DoesNotExist:
                pass

        return Response(stores)