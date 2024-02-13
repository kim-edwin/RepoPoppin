from django.db import models
from django.utils import timezone
from common.models import CommonModel

class Store(CommonModel):

    """
    Store Model Definition
    """

    name = models.CharField(max_length=180, default="")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    img_url = models.URLField(default="")
    article_url = models.URLField(default="")
    poi_address = models.CharField(max_length=100, default="")
    hash_tags = models.CharField(max_length=300, default="")
    is_visible = models.BooleanField(default=False)

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
    
    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = timezone.now().date()
        if not self.end_date:
            self.end_date = timezone.now().date() + timezone.timedelta(days=30)
        super().save(*args, **kwargs)

