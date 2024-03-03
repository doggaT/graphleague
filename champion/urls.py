from django.urls import path
from .views import ChampionsView

urlpatterns = [
    path('', ChampionsView.as_view(), name='champions')
]