from rest_framework.serializers import ModelSerializer
from stores.serializers import TinyStoreSerializer
from users.serializers import TinyUserSerializer
from .models import Report

class ReportSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    store = TinyStoreSerializer(read_only=True)
    

    class Meta:
        model = Report
        fields = (
            "pk",
            "store",
            "user",
            "payload",
        )