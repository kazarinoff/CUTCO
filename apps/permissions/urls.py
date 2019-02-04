from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.permissionsedit, name='home'),
    path('add',views.permissionsadd,name='add'),
    path('departments/<did>/index',views.permissionsdeptadd,name='addbydept'),
    path('update',views.permissionsupdate,name='update')
]
