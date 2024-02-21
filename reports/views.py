from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from reports.serializers import ReportSerializer
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Review

# Create your views here.
class Report(APIView):

    permission_classes = [IsAuthenticated] 

    def post(self, request):

        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            report = serializer.save(
                user=request.user,
                )
            serializer = ReportSerializer(report)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)