from django.urls import path
from . import views

urlpatterns = [
    path("", views.team_builder, name="team-builder")
]
