from django.shortcuts import render, HttpResponse, redirect
from apps.loginregister.models import *
from datetime import datetime
import bcrypt
from django.core.exceptions import ObjectDoesNotExist
from apps.Courses.models import *

def permissionsindex(request):
    x= User.objects.get(id=request.session['loggedid'])
    cd=College.objects.values('name','departments__name','departments__id','departments__users__id','departments__users__first_name','departments__users__last_name','departments__users__username','departments__users__permission__level','departments__users__permission__levelname')
    return render(request,'permissionsindex.html',{'user':x,'newdict':cd})

def permissionsadd(request):
    if request.method=='POST':
        x=User.objects.get(id=request.session['loggedid'])
        y=User.objects.get(id=request.POST['userid'])
        d=Dept.objects.get(id=request.POST['deptid'])
        try:
            p=Permission.objects.get(user=x,dept=d)
        except ObjectDoesNotExist:
            p=False
        if not p or p.level<5:
            return HttpResponse('YOU ARE NOT ALLOWED ADD ROLES IN THIS DEPARTMENT.')
        if p.level>=5:
            q=Permission.objects.create(user=y,dept=d,level=request.POST['level'])
            if int(request.POST['level'])==10:
                q.levelname='God'
            elif int(request.POST['level'])==8:
                q.levelname='Administrator'
            elif int(request.POST['level'])==5:
                q.levelname='Faculty'
            else:
                q.levelname='Student'
            q.save()
            print(p,'permiiisssion')
        else:
            return HttpResponse('YOU ARE NOT ALLOWED ADD ROLES IN THIS DEPARTMENT.')
        return redirect(request.POST['nextpath'])
    return redirect('/courses/')

def permissionsdeptindex(request,did):
    x=User.objects.get(id=request.session['loggedid'])
    d=Dept.objects.get(id=did)
    try:
        p=Permission.objects.get(user=x,dept=d)
    except ObjectDoesNotExist:
        p={}
    nu=User.objects.exclude(permissions=d).all()
    cu=Permission.objects.filter(dept=d).all()
    return render (request, 'permissionsdeptindex.html',{'dept':d,'newusers':nu,'currentusers':cu,'user':x,'accesslevel':p})

def permissionsupdate(request):
    if request.method=='POST':
        x=User.objects.get(id=request.session['loggedid'])
        d=Dept.objects.get(id=request.POST['deptid'])
        try:
            p=Permission.objects.get(user=x,dept=d)
        except ObjectDoesNotExist:
            return HttpResponse("Error, you are unworthy")
        if p.level <= int(request.POST['level']):
            return HttpResponse('Error')
        q=Permission.objects.get(user_id=request.POST['userid'],dept=d)
        q.level=int(request.POST['level'])
        if q.level==10:
            q.levelname='God'
        elif q.level==8:
            q.levelname='Administrator'
        elif q.level==5:
            q.levelname='Faculty'
        else:
            q.levelname='Student'
        q.save()
        return redirect(request.POST['nextpath'])
    return redirect('/treqtable/')

def permissionsdelete(request,pid):
    if request.method =='POST':
        x=User.objects.get(id=request.session['loggedid'])
        pd=Permission.objects.get(id=pid)
        try:
            p=Permission.objects.get(user=x,dept=pd.dept)
        except ObjectDoesNotExist:
            p=False
        if not p or p.level<10 or pid != request.POST['permissionid']:
            return HttpResponse('YOU ARE NOT ALLOWED DELETE THIS ROLE.')
        else:
            pd.delete()
            return redirect(request.POST['nextpath'])


