from django.apps import AppConfig

from Recommend.models import RecommenderNet


class StoresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stores'
    model = RecommenderNet(num_users=1010, num_news=253, embedding_size=100)
