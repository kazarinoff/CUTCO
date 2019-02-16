from django.contrib import admin
from django.urls import path, include
from . import views

<<<<<<< HEAD
app_name = 'loginapp'
=======
app_name ='loginapp'

>>>>>>> 0794d1ad94323d0a62a06f790678c0f2c847a8bb
urlpatterns = [
    path('',views.index, name='index'),
    path('regval/',views.regval, name='regval'),
    path('loginval/',views.loginval, name='loginval'),
    path('logout/',views.logout, name='logout'),
    path('profile/<uid>',views.showuser,name='showprofile'),
    path('profile/<uid>/edit',views.edituser,name='edituser'),
    path('update/',views.updateuser,name='updateuser'),
]
