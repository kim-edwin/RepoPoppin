from django.db import models
from common.models import CommonModel

class Report(CommonModel):
    store = models.ForeignKey("stores.Store", 
                            null=True,
                            blank=True,
                            on_delete=models.CASCADE,
                            related_name="reports",)
    user = models.ForeignKey("users.User",
                        null=True,
                        blank=True,
                        on_delete=models.CASCADE,
                        related_name="reports",)
    payload = models.TextField()