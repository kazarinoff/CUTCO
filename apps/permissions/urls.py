from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.permissionsindex, name='home'),
    path('add',views.permissionsadd,name='add'),
    path('departments/<did>/index',views.permissionsdeptindex,name='addbydept'),
    path('update',views.permissionsupdate,name='update'),
    path('<pid>/delete',views.permissionsdelete,name='delete')
]
