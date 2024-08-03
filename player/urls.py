from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_stats, name="my-stats"),
    path("<str:match_id>/", views.my_match_stats, name="my_match_stats")
]
