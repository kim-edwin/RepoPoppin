from django.db import models
from common.models import CommonModel

class Review(CommonModel):

    user = models.ForeignKey("users.User", 
                            on_delete=models.CASCADE,
                            related_name="reviews",)
    store = models.ForeignKey("stores.Store", 
                            null=True,
                            blank=True,
                            on_delete=models.CASCADE,
                            related_name="reviews",)
    payload = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.user} / {self.rating}"