from django.urls import path

from categories import views

urlpatterns = [
    path("", views.Categories.as_view(), name="categories"),
    path("<int:category_id>", views.CategoryDetail.as_view(), name="category"),
]
