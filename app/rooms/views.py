from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from categories.models import Category
from medias.serializers import PhotoSerializer
from reviews.seirializers import ReviewsSerializer
from rooms.models import Amenity, Room
from rooms.serializers import AmenitySerializer, RoomsSerializer, RoomDetailSerializer

ROOM_TAG = "Rooms"
ROOM_AMENITY_TAG = f"{ROOM_TAG}/Amenities"
ROOM_REVIEW_TAG = f"{ROOM_TAG}/Reviews"
ROOM_PHOTO_TAG = f"{ROOM_TAG}/Photos"


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
        except Amenity.DoesNotExist:
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
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    @swagger_auto_schema(
        tags=[ROOM_TAG],
    )
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomsSerializer(rooms, many=True, context={"request": request})

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        tags=[ROOM_TAG],
        request_body=RoomDetailSerializer,
    )
    def post(self, request):
        # 무언가를 생성하기 위해서 데이터는 serializer를 통해서 전달되어야함
        # serializer는 validation 해줄거고(데이너가 정확한지, 유저가 보낸 데이터로 방을 생성할 수 있는지)

        serializer = RoomDetailSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            category_id = request.data.get("category")
            if not category_id:
                raise ParseError("Category is required")

            category = get_object_or_404(Category, id=category_id)
            if category.kind != Category.CategoryKindChoices.ROOM:
                raise ParseError("Category kind should be 'rooms'")

            try:
                with transaction.atomic():
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )
                    amenities = request.data.get("amenities")
                    for amenity_id in amenities:
                        amenity = Amenity.objects.get(id=amenity_id)
                        room.amenities.add(amenity)
                    serializer = RoomDetailSerializer(room)
                    return Response(
                        serializer.data,
                        status=status.HTTP_200_OK,
                    )
            except Exception:
                raise ParseError("Amenity not found")
        return Response(
            serializer.errors,
        )


class RoomDetail(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    @staticmethod
    def get_object(room_id):
        try:
            return Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        tags=[ROOM_TAG],
    )
    def get(self, request, room_id):
        room = self.get_object(room_id)
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        tags=[ROOM_TAG],
    )
    def put(self, request, room_id):
        room = self.get_object(room_id)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied

    @swagger_auto_schema(
        tags=[ROOM_TAG],
    )
    def patch(self, request, room_id):
        pass

    @swagger_auto_schema(
        tags=[ROOM_TAG],
    )
    def delete(self, request, room_id):
        room = self.get_object(room_id)

        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=status.HTTP_200_OK)


class RoomReviews(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    @staticmethod
    def get_object(room_id):
        try:
            return Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        tags=[ROOM_REVIEW_TAG],
    )
    def get(self, request, room_id):
        try:
            page = request.query_params.get("page")
            page = int(page)
        except ValueError:
            page = 1

        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(room_id)
        serializer = ReviewsSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(tags=[ROOM_REVIEW_TAG], request_body=ReviewsSerializer)
    def post(self, request, room_id):
        serializer = ReviewsSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_object(room_id),
            )
            serializer = ReviewsSerializer(review)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors)


class RoomPhotos(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    @staticmethod
    def get_object(room_id):
        return get_object_or_404(Room, id=room_id)

    @swagger_auto_schema(tags=ROOM_PHOTO_TAG, request_body=PhotoSerializer)
    def post(self, request, room_id):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        room = self.get_object(room_id)
        if request.user != room.owner:
            raise PermissionDenied

        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
