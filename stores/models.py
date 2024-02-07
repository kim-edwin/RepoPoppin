from django.db import models
from common.models import CommonModel

class Store(CommonModel):

    """
    Store Model Definition
    """

    name = models.CharField(max_length=180, default="")
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def total_amenities(self):
        return self.amenities.count()
    
    def rating(self):
        count = self.reviews.count()
        if count == 0:
            return 0
        else:
            total_rating = 0
            for review in self.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2)

