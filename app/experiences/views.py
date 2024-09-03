from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from experiences.models import Perk, Experience
from experiences.serializers import (
    PerksSerializer,
    ExperienceDetailSerializer,
    CreateExperienceSerializer,
)

EXPERIENCES_TAGS = "Experiences"
PERKS_TAGS = f"{EXPERIENCES_TAGS} / Perks"


class Perks(APIView):
    @swagger_auto_schema(
        tags=[PERKS_TAGS],
    )
    def get(self, request):
        perks = Perk.objects.all()
        serializer = PerksSerializer(
            perks,
            many=True,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        tags=[PERKS_TAGS],
        request_body=PerksSerializer,
    )
    def post(self, request):
        serializer = PerksSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            perk = serializer.save()
            serializer = PerksSerializer(perk)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
        )


class PerkDetail(APIView):
    def get_object(self, perk_id):
        try:
            return Perk.objects.get(id=perk_id)
        except Perk.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        tags=[PERKS_TAGS],
    )
    def get(self, request, perk_id):
        perk = self.get_object(perk_id)
        serializer = PerksSerializer(perk)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        tags=[PERKS_TAGS],
        request_body=PerksSerializer,
    )
    def put(self, request, perk_id):
        perk = self.get_object(perk_id)
        serializer = PerksSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            perk = serializer.save()
            serializer = PerksSerializer(perk)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
        )

    @swagger_auto_schema(
        tags=[PERKS_TAGS],
        request_body=PerksSerializer,
    )
    def patch(self, request, perk_id):
        perk = self.get_object(perk_id)
        serializer = PerksSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            perk = serializer.save()
            serializer = PerksSerializer(perk)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
        )

    @swagger_auto_schema(
        tags=[PERKS_TAGS],
    )
    def delete(self, request, perk_id):
        perk = self.get_object(perk_id)
        perk.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class Experiences(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(tags=[EXPERIENCES_TAGS])
    def get(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceDetailSerializer(experiences, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=[EXPERIENCES_TAGS], request_body=CreateExperienceSerializer
    )
    def post(self, request):
        serializer = CreateExperienceSerializer(data=request.data)
        if serializer.is_valid():
            experience = serializer.save()
            return Response({"success": True}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
