from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("summoner/", views.summoner_search, name="summoner_search"),
    path("<str:puuid>/matches/", views.summoner_info, name="summoner_info"),
    path("<str:puuid>/matches/<str:match_id>/", views.summoner_match, name="summoner_match"),
]
