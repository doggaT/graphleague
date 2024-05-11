from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.champions, name="champions"),
    path('<str:champion>/', views.champion_details, name="champion")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
