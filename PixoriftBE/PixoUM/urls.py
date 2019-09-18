from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('', FollowView.as_view())
]

print('Pixorift User Management loaded.')
