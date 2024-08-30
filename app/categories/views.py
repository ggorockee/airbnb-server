from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from categories.models import Category
from categories.serializers import CategorySerializer


class Categories(APIView):
    @swagger_auto_schema(
        tags=["Category"],
        request_body=None,
    )
    def get(self, request):
        all_categories = Category.objects.all()
        serializer = CategorySerializer(
            all_categories,
            many=True,
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["Category"],
        request_body=CategorySerializer,
    )
    def post(self, request):
        serializer = CategorySerializer(
            data=request.data,
        )
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(
                CategorySerializer(new_category).data,
            )

        return Response(
            serializer.errors,
        )


class CategoryDetail(APIView):
    def get_object(self, category_id):
        try:
            return Category.objects.get(
                id=category_id,
            )
        except Category.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        tags=["Category"],
        request_body=None,
    )
    def get(self, request, category_id):
        serializer = CategorySerializer(
            self.get_object(category_id),
        )
        return Response(
            serializer.data,
        )

    @swagger_auto_schema(
        tags=["Category"],
        request_body=CategorySerializer,
    )
    def patch(self, request, category_id):
        serializer = CategorySerializer(
            Category,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(
                CategorySerializer(updated_category).data,
            )
        return Response(
            serializer.errors,
        )

    @swagger_auto_schema(tags=["Category"], request_body=CategorySerializer)
    def delete(self, request, category_id):
        self.get_object(category_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
