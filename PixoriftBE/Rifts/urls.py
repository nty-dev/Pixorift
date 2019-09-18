from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('', RiftView.as_view()),
    path('rate/', RiftRatingView.as_view()),
]

print('Rifts systems loaded.')
