from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'loginapp'
urlpatterns = [
    path('',views.index, name='index'),
    path('regval/',views.regval, name='regval'),
    path('loginval/',views.loginval, name='loginval'),
    path('logout/',views.logout, name='logout'),
    path('profile/<uid>',views.showuser,name='showprofile'),
    path('profile/<uid>/edit',views.edituser,name='edituser'),
    path('update/',views.updateuser,name='updateuser'),
]
