from django.core.serializers import serialize
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rooms.models import Amenity, Room
from rooms.serializers import AmenitySerializer, RoomsSerializer, RoomDetailSerializer

ROOM_TAG = "Rooms"
ROOM_AMENITY_TAG = f"{ROOM_TAG}/Amenities"


class Amenities(APIView):
    @swagger_auto_schema(
        tags=[ROOM_AMENITY_TAG],
    )
    def get(self, request):
        amenities = Amenity.objects.all()
        serializer = AmenitySerializer(
            amenities,
            many=True,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        tags=[ROOM_AMENITY_TAG],
        request_body=AmenitySerializer,
    )
    def post(self, request):
        serializer = AmenitySerializer(
            data=request.data,
        )
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                AmenitySerializer(amenity).data,
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
        )


class AmenityDetail(APIView):
    def get_object(self, amenity_id):
        try:
            return Amenity.objects.get(id=amenity_id)
        except Amenity.DoesNotExists:
            raise NotFound

    @swagger_auto_schema(
        tags=[ROOM_AMENITY_TAG],
    )
    def get(self, request, amenity_id):
        amenity = self.get_object(amenity_id)
        serializer = AmenitySerializer(amenity)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        tags=[ROOM_AMENITY_TAG],
        request_body=AmenitySerializer,
    )
    def put(self, request, amenity_id):
        amenity = self.get_object(amenity_id)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_amenity = serializer.save()
            serializer = AmenitySerializer(updated_amenity)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
        )

    @swagger_auto_schema(
        tags=[ROOM_AMENITY_TAG],
        request_body=AmenitySerializer,
    )
    def patch(self, request, amenity_id):
        amenity = self.get_object(amenity_id)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_amenity = serializer.save()
            serializer = AmenitySerializer(updated_amenity)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
        )

    @swagger_auto_schema(
        tags=[ROOM_AMENITY_TAG],
    )
    def delete(self, request, amenity_id):
        amenity = self.get_object(amenity_id)
        amenity.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class Rooms(APIView):
    @swagger_auto_schema(
        tags=[ROOM_TAG],
    )
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomsSerializer(
            rooms,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        tags=[ROOM_TAG],
    )
    def post(self, request):
        pass


class RoomDetail(APIView):
    def get_object(self, room_id):
        try:
            return Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        tags=[ROOM_TAG],
    )
    def get(self, request, room_id):
        room = self.get_object(room_id)
        serializer = RoomDetailSerializer(room)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        tags=[ROOM_TAG],
    )
    def put(self, request, room_id):
        pass

    @swagger_auto_schema(
        tags=[ROOM_TAG],
    )
    def patch(self, request, room_id):
        pass

    @swagger_auto_schema(
        tags=[ROOM_TAG],
    )
    def delete(self, request, room_id):
        pass
