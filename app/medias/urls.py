from django.urls import path
from medias import views

urlpatterns = [
    path("photos/<int:photo_id>/", views.PhotoDetail.as_view()),
]
