from django.db import models

class CommonModel(models.Model):
    """
    Common Model Definition
    """
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True) #최초 생성시에 현재시가 입력되고 불변
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) #저장할 때마다 현재시로 업데이트 됨

    class Meta:
        abstract = True 
        #Django가 이 model을 봐도 데이터베이스에 저장하지 않게끔 옵션을 수정한다.
        #오로지 다른 App의 모델들이 이 모델을 참고하게 하고 싶기 때문이다.