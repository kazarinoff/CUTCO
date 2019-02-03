from django.shortcuts import render, HttpResponse, redirect
from apps.loginregister.models import *
from datetime import datetime
import bcrypt
from apps.Courses.models import *

def permissionsedit(request):
    x= User.objects.get(id=request.session['loggedid'])
    y= x.permissions.all()
    yi=[]
    for i in y:
        p=Permission.objects.filter(dept=i)
        print('permissionshere',p)
        yi.append({'deptname':i.name,'collegename':i.college.name,'usersallowed':p})
    permissions=Permission.objects.filter(user=x)
    return render(request,'permissionupdate.html',{'user':x,'permissions':yi})

def permissionsshow(request):
    x=User.objects.get(id=request.session['loggedid'])
    y=Dept.objects.all()
    yi=[]
    for i in y:
        yp=y.permissions.all()
        yi.append({'deptname':y.name,'collegename':y.college.name,'usersallowed':yp})
    permissions=Permission.objects.filter(user=x)
    return render(request,'permissionsshow.html',{'user':x,'permissions':yi})
