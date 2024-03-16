from django.db import models
from stores.models import Store
from users.models import User

class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accesslogs",)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="accesslogs",)
    accessed_at = models.DateTimeField(auto_now_add=True)
