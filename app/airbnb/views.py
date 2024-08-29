from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class HelathCheck(APIView):
    @swagger_auto_schema(tags=["HealthCheck"])
    def get(self, request):
        resp = {"status": "active"}
        return Response(resp, status=status.HTTP_200_OK)
