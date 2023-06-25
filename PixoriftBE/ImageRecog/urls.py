from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
#from .PixoAI import PixoAI as P

urlpatterns = [
    path('', ImageSubmit.as_view()),
    path('quest/', QuestRequest.as_view())
]

print('Image Recognition Engine Initiated.')
