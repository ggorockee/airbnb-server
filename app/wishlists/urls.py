from django.urls import path
from wishlists import views

urlpatterns = [
    path("", views.WishList.as_view()),
    path("<int:wishlist_id>/", views.WishListDetail.as_view()),
    path("<int:wishlist_id>/rooms/<int:room_id>/", views.WishListToggle.as_view()),
]
