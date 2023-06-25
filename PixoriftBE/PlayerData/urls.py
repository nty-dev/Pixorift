from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('info/', PlayerDataInfo.as_view()),
    path('admin_add/', AdminPDAddition.as_view()),
    path('lb/', PlayerDataLB.as_view())
]

print('Player Data loaded.')
