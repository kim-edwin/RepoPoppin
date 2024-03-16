from django.db import models
from stores.models import Store

class TopStore(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    rank = models.IntegerField()
