from django.urls import path
from .views import getTrendRepo

urlpatterns = [
    path('',getTrendRepo,name='trend'),
]