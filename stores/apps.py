from django.apps import AppConfig

from Recommend.models import RecommenderNet


class StoresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stores'
    model = RecommenderNet(num_users=39492, num_news=10467, embedding_size=30)
