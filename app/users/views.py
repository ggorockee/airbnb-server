from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


from users.serializers import (
    PrivateUserSerializer,
    PublicUserSerializer,
    ChangePasswordSerializer,
    SignInSerializer,
)

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
    @swagger_auto_schema(tags=[USER_TAG])
    def get(self, request, username: str):
        user = get_user_model().objects.get(username=username)
        serializer = PublicUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    @swagger_auto_schema(tags=[USER_TAG], request_body=ChangePasswordSerializer)
    def put(self, request):
        serializer = ChangePasswordSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get("new_password1"))
            user.save()
            return Response({"success": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignIn(APIView):
    @swagger_auto_schema(tags=[USER_TAG], request_body=SignInSerializer)
    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        if not email or not password:
            raise ParseError("No authentication credentials were provided.")

        serializer = SignInSerializer(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            login(request, serializer.validated_data.get("user"))
            return Response({"success": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignOut(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    @swagger_auto_schema(tags=[USER_TAG])
    def post(self, request):
        logout(request)
        return Response({"success": True}, status=status.HTTP_200_OK)
