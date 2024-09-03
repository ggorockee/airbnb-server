from django.urls import path
from experiences import views


# GET POST /experiences
# GET PUT DELETE /experiences/1
# GET /experiences/1/perks
# GET POST /experiences/perks                           [v]
# GET PUT DELETE /experiences/perks/1                   [v]
# GET POST /experiences/1/bookings
# GET PUT DELETE /experiences/1/bookings/2

urlpatterns = [
    path("", views.Experiences.as_view()),
    # path("<int:experience_id>/", views.ExperienceDetail.as_view()),
    # path("<int:experience_id>/perks/", views.ExperienceDetail.as_view()),
    # path("<int:experience_id>/bookings/", views.ExperienceDetail.as_view()),
    # path(
    #     "<int:experience_id>/bookings/<int:booking_id>/",
    #     views.ExperienceDetail.as_view(),
    # ),
    path("perks/", views.Perks.as_view()),
    path("perks/<int:perk_id>/", views.PerkDetail.as_view()),
]
