from django.urls import path
from . import views

urlpatterns = [
    path('', views.champions, name="champions"),
    path('<str:champion>/', views.champion_details, name="champion")
]
