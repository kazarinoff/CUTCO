from django.shortcuts import render, HttpResponse, redirect
from apps.loginregister.models import *
from datetime import datetime
import bcrypt
from django.core.exceptions import ObjectDoesNotExist
from apps.Courses.models import *

def permissionsindex(request):
    x,xc,xd ={},{},{}
    p={'god':[],'administrator':[],'faculty':[],'any':[]}
    if 'loggedid' in request.session:
        x= User.objects.get(id=request.session['loggedid'])
        xc=College.objects.filter(users=x)
        xd=Dept.objects.filter(users=x)
        for i in Permission.objects.filter(user=x):
            p['any'].append(i.dept_id)
            if i.level==10:
                p['god'].append(i.dept_id)
            if i.level==8:
                p['administrator'].append(i.dept_id)
            if i.level==5:
                p['faculty'].append(i.dept_id)
    c=College.objects.values('name','departments__name','departments__id','departments__users__id','departments__users__first_name','departments__users__last_name','departments__users__username','departments__users__permission__level','departments__users__permission__levelname','departments__users__permission__dept_id')
    return render(request,'permissionsindex.html',{'usercolleges':xc,'userdepts':xd,'user':x,'newdict':c,'permissions':p})

def permissionsadd(request):
    if request.method=='POST':
        x=User.objects.get(id=request.session['loggedid'])
        y=User.objects.get(id=request.POST['userid'])
        d=Dept.objects.get(id=request.POST['deptid'])
        try:
            p=Permission.objects.get(user=x,dept=d,level__gt=4)
        except ObjectDoesNotExist:
            return HttpResponse('YOU ARE NOT ALLOWED ADD ROLES IN THIS DEPARTMENT.')
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
        return redirect(request.POST['nextpath'])
    return redirect('courses:home')

def permissionsdeptindex(request,did):
    p,x,xc,xd = {},{},{},{}
    if 'loggedid' in request.session:
        x= User.objects.get(id=request.session['loggedid'])
        xc=College.objects.filter(users=x)
        xd=Dept.objects.filter(users=x)
    d=Dept.objects.get(id=did)
    try:
        p=Permission.objects.get(user=x,dept=d)
    except ObjectDoesNotExist:
        pass
    nu=User.objects.exclude(permissions=d).all()
    cu=Permission.objects.filter(dept=d).all()
    return render (request, 'permissionsdeptindex.html',{'usercolleges':xc,'userdepts':xd,'dept':d,'newusers':nu,'currentusers':cu,'user':x,'accesslevel':p})

def permissionsupdate(request):
    if request.method=='POST':
        x=User.objects.get(id=request.session['loggedid'])
        d=Dept.objects.get(id=request.POST['deptid'])
        try:
            p=Permission.objects.get(user=x,dept=d)
        except ObjectDoesNotExist:
            return HttpResponse("Error")
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
    return redirect('courses:treqtable')

def permissionsdelete(request,pid):
    if request.method =='POST':
        x=User.objects.get(id=request.session['loggedid'])
        pd=Permission.objects.get(id=pid)
        try:
            p=Permission.objects.get(user=x,dept=pd.dept,level__gt=9)
        except ObjectDoesNotExist:
            return HttpResponse('YOU ARE NOT ALLOWED DELETE THIS ROLE.')
        if p.id != request.POST['permissionid']:
            return HttpResponse('YOU ARE NOT ALLOWED DELETE THIS ROLE.')
        pd.delete()
        return redirect(request.POST['nextpath'])
    return redirect('courses:home')