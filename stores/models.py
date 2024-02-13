from django.db import models
from django.utils import timezone
from common.models import CommonModel

class Store(CommonModel):

    """
    Store Model Definition
    """

    STATUS_CHOICES = (
        ('READY', '준비중'),
        ('IN_PROGRESS', '진행중'),
        ('COMPLETED', '종료'),
    )

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
    
    def save(self, *args, **kwargs): #startdate, enddate 정보가 없으면 default 값으로 오늘부터 일주일로 함
        if not self.start_date:
            self.start_date = timezone.now().date()
        if not self.end_date:
            self.end_date = timezone.now().date() + timezone.timedelta(days=30)
        super().save(*args, **kwargs)

    def status(self):
            today = timezone.now().date()
            if today < self.start_date:
                remaining_days = (self.start_date - today).days
                return f'준비중 D-{remaining_days}'
            elif self.start_date <= today <= self.end_date:
                return '진행중'
            else:
                return '종료'
