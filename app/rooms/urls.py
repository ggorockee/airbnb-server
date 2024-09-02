from django.urls import path
from rooms import views


urlpatterns = [
    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:amenity_id>/", views.AmenityDetail.as_view()),
    path("<int:room_id>/", views.RoomDetail.as_view()),
    path("<int:room_id>/reviews/", views.RoomReviews.as_view()),
    path("<int:room_id>/photos/", views.RoomPhotos.as_view()),
    path("", views.Rooms.as_view()),
]
