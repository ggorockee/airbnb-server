from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from medias.models import Photo

MEDIA_PHOTO_TAG = "Medias / Photos"


class PhotoDetail(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def get_object(photo_id):
        return get_object_or_404(Photo, id=photo_id)

    @swagger_auto_schema(tags=[MEDIA_PHOTO_TAG])
    def delete(self, request, photo_id):
        photo = self.get_object(photo_id)
        if (photo.room and photo.room.owner != request.user) or (
            photo.experience and photo.experience.host != request.user
        ):
            raise PermissionDenied

        photo.delete()
        return Response(status=status.HTTP_200_OK)
