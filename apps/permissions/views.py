from django.shortcuts import render, HttpResponse, redirect
from apps.loginregister.models import *
from datetime import datetime
import bcrypt
from apps.Courses.models import *

def permissionsedit(request):
    x= User.objects.get(id=request.session['loggedid'])
    cd=College.objects.values('name','departments__name','departments__id','departments__users__id','departments__users__first_name','departments__users__last_name','departments__users__username','departments__users__permission__level')
    return render(request,'permissionsindex.html',{'user':x,'newdict':cd})

def permissionsadd(request):
    if request.method=='POST':
        print('postrequest',request.POST)
        x=User.objects.get(id=request.session['loggedid'])
        y=User.objects.get(id=request.POST['userid'])
        d=Dept.objects.get(id=request.POST['deptid'])
        p=Permission.objects.create(user=y,dept=d,level=request.POST['level'])
        p.save()
        return redirect(request.POST['nextpath'])
    return redirect('/courses/')

def permissionsdeptadd(request,did):
    d=Dept.objects.get(id=did)
    nu=User.objects.exclude(permissions=d).all()
    cu=Permission.objects.filter(dept=d).all()
    return render (request, 'permissionsdeptindex.html',{'dept':d,'newusers':nu,'currentusers':cu})

def permissionsupdate(request):
    if request.method=='POST':
        p=Permission.objects.get(user_id=request.POST['userid'],dept_id=request.POST['deptid'])
        p.level=request.POST['level']
        p.save()
        return redirect(request.POST['nextpath'])
