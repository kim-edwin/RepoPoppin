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

    news_id = models.CharField(max_length = 50, default="", null=True, blank=True)
    news_keyword = models.TextField(null=True, blank=True)
    news_feature = models.TextField(null=True, blank=True)
    p_name = models.CharField(max_length=180, default="", null=True, blank=True)
    p_startdate = models.DateField(null=True, blank=True)
    p_enddate = models.DateField(null=True, blank=True)
    img_url = models.URLField(default="", null=True, blank=True)
    news_url = models.URLField(default="")
    p_location = models.CharField(max_length=100, default="", null=True, blank=True)
    p_hashtag = models.CharField(max_length=300, default="", null=True, blank=True)
    p_chucheon = models.TextField(null=True, blank=True,)
    is_visible = models.BooleanField(default=False)

    def __str__(self):
        return self.p_name
    
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
        if not self.p_startdate:
            self.p_startdate = timezone.now().date()
        if not self.p_enddate:
            self.p_enddate = timezone.now().date() + timezone.timedelta(days=30)
        super().save(*args, **kwargs)

    def status(self):
            today = timezone.now().date()
            if today < self.p_startdate:
                remaining_days = (self.p_startdate - today).days
                return f'준비중 D-{remaining_days}'
            elif self.p_startdate <= today <= self.p_enddate:
                return '진행중'
            else:
                return '종료'
    
    def thumbnail(self):
        if self.img_url:
            # 이미지 URL을 콤마로 분할하여 리스트로 만듭니다.
            img_urls = self.img_url.split(',')
            # 첫 번째 이미지 URL을 가져옵니다.
            first_img_url = img_urls[0].strip()
            return first_img_url
        else:
            return None

