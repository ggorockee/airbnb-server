from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from rooms.models import Room
from wishlists.models import Wishlist
from wishlists.serializers import WishlistSerializer

WISHLIST_TAG = "WishList"
WISHLIST_TOGGLE_TAG = "WishList / Toggle"


class WishList(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=[WISHLIST_TAG])
    def get(self, request):
        wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            wishlists,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    @swagger_auto_schema(tags=[WISHLIST_TAG], request_body=WishlistSerializer)
    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(user=request.user)
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WishListDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(wishlist_id, user):
        return get_object_or_404(Wishlist, id=wishlist_id, user=user)

    @swagger_auto_schema(tags=[WISHLIST_TAG])
    def get(self, request, wishlist_id):
        wishlist = self.get_object(wishlist_id, request.user)
        serializer = WishlistSerializer(
            wishlist,
            context={"request": request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=[WISHLIST_TAG], request_body=WishlistSerializer)
    def put(self, request, wishlist_id):
        wishlist = self.get_object(wishlist_id, request.user)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=[WISHLIST_TAG], request_body=WishlistSerializer)
    def patch(self, request, wishlist_id):
        pass

    @swagger_auto_schema(tags=[WISHLIST_TAG])
    def delete(self, request, wishlist_id):
        wishlist = self.get_object(wishlist_id, request.user)
        wishlist.delete()
        return Response(status=status.HTTP_200_OK)


class WishListToggle(APIView):
    @staticmethod
    def get_list(room_id, user):
        return get_object_or_404(Wishlist, id=room_id, user=user)

    @staticmethod
    def get_room(room_id):
        return get_object_or_404(Room, id=room_id)

    @swagger_auto_schema(tags=[WISHLIST_TOGGLE_TAG])
    def put(self, request, wishlist_id, room_id):
        wishlist = self.get_list(room_id, request.user)
        room = self.get_room(room_id)
        if wishlist.rooms.filter(id=room.id).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=status.HTTP_200_OK)
