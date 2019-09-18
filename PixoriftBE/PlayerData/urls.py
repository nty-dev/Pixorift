from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('', Get_Level.as_view()),
    path('admin/', EditLevel.as_view()),
]

print('Player Data loaded.')
