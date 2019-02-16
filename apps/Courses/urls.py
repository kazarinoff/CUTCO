from django.contrib import admin
from django.urls import path, include
from . import views

app_name ='courses'

urlpatterns = [
    path('',views.home, name='home'),
    path('<cid>/add',views.addcourseform, name='addcourseform'),
    path('include/',views.addcourse, name='addcourse'),
    path('treqtable/',views.treqtable,name='treqtable'),
    path('treqtablegenerate/',views.treqtablegenerate, name='treqtablegenerate'),
    path('<idnumber>/update/',views.updatecourse,name='updatecourse'),
    path('<idnumber>/edit/',views.editcourse,name='editcourse'),
    path('<idnumber>/delete/',views.deletecheck, name='deletecheck'),
    path('<idnumber>/destroy/',views.deletecourse, name='deletecourse'),
    path('<idnumber>/treq',views.viewtreq, name='viewtreq'),
    path('<idnumber>/treqedit',views.edittreq, name='edittreq'),
    path('<idnumber>/',views.viewcourse, name='viewcourse')
]