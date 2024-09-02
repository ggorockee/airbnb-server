from django.contrib.auth import get_user_model
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


from users.serializers import PrivateUserSerializer, PublicUserSerializer

ME_TAG = "Users / Me"
USER_TAG = "Users"


class Me(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=[ME_TAG])
    def get(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(tags=[ME_TAG], request_body=PrivateUserSerializer)
    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            user = serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=[ME_TAG], request_body=PrivateUserSerializer)
    def patch(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            user = serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Users(APIView):
    @swagger_auto_schema(tags=[USER_TAG], request_body=PrivateUserSerializer)
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError("password must required.")

        serializer = PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicUser(APIView):
    def get(self, request, username: str):
        user = get_user_model().objects.get(username=username)
        serializer = PublicUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
