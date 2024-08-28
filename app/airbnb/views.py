from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HelathCheck(APIView):
    def get(self, request):
        resp = {
        "status": "active"
        }
        return Response(resp, status=status.HTTP_200_OK)