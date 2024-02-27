from django.db import models
from stores.models import Store
from users.models import User

class StoreAccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)

    
