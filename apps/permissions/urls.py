from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.permissionsedit, name='home'),
    path('show',views.permissionsshow, name='show')
]
