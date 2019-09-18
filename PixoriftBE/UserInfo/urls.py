from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
	path('userinfo/', privateusercall.as_view()),
    path('otheruserinfo/', publicusercall.as_view()),
    path('login/', logincall.as_view()),
    path('logout/', logout.as_view()),
    path('create_account/', create_account.as_view()),
    path('update_account/', change_account.as_view()),
    path('delete_account/', delete_account.as_view()),
    path('change_password/', change_password.as_view()),
	path('usernameavailcheck/', usernameavail.as_view())
]

print('User Accounts Initiated.')
