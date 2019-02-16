from django.shortcuts import render, HttpResponse, redirect
from apps.loginregister.models import *
from datetime import datetime
import bcrypt
from apps.Courses.models import *
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    if 'loggedid' in request.session:
        return redirect('courses:home')
    if 'errors' not in request.session:
        request.session['errors']={}
    return render(request,'login.html',{'colleges':College.objects.all(),'errors':request.session['errors']})

def regval(request):
    validator= ValidationManager()
    if request.method=='POST':
        request.session['errors']={}
        errors= validator.validatereg(request.POST)
        if not len(errors):
            pwd=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            pwdcrpt=pwd.decode('utf-8')
            x=User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'], username=request.POST['username'], passwordhash=pwdcrpt)
            if request.POST['college'] != 'atlarge':
                c=College.objects.get(id=request.POST['college'])
                x.colleges.add(c)
                for d in c.departments.all():
                    q=Permission.objects.create(user=x,dept=d,level=request.POST['role'])
                    if int(request.POST['role'])==10:
                        q.levelname='God'
                    elif int(request.POST['role'])==8:
                        q.levelname='Administrator'
                    elif int(request.POST['role'])==5:
                        q.levelname='Faculty'
                    elif int(request.POST['role'])==1:
                        q.levelname='Student'
                    else:
                        q.levelname='At large'
                    q.save()
            x.save()
            request.session['loggedid']=User.objects.last().id
            return redirect('courses:treqtable')
        else:
            request.session['errors']=errors
            return redirect('loginapp:index')
    return redirect('loginapp:index')

def loginval(request):
    validator= ValidationManager()
    request.session['errors']={}
    if request.method=='POST':
        errors= validator.validatelogin(request.POST)
        if not len(errors):
            request.session['loggedid']=User.objects.get(username=request.POST['username']).id
            return redirect ('courses:treqtable')
        else:
            request.session['errors']=errors
    return redirect('loginapp:index')

def logout(request):
    request.session.clear()
    return redirect('loginapp:index')

def showuser(request,uid):
    p,x,xc,xd={},{},{},{}
    if 'loggedid' in request.session:
        x= User.objects.get(id=request.session['loggedid'])
        xc=College.objects.filter(users=x)
        xd=Dept.objects.filter(users=x)
    y=User.objects.get(id=uid)
    try:
        p=Permission.objects.filter(user=x).values('levelname','dept__name','dept__college__name')
    except:
        pass
    return render(request,'showuser.html',{'usercolleges':xc,'userdepts':xd,'user':x,'profileuser':y,'permissions':p})

def edituser(request,uid):
    if 'errors' not in request.session:
        request.session['errors']={}
    if 'loggedid' not in request.session:
        return redirect('courses:home')
    if int(uid) !=request.session['loggedid']:
        return redirect('courses:home')
    x=User.objects.get(id=request.session['loggedid'])
    xc=College.objects.filter(users=x)
    xd=Dept.objects.filter(users=x)
    return render (request,'useredit.html',{'usercolleges':xc,'userdepts':xd,'errors':request.session['errors'], 'user':x})

def updateuser(request):
    validator= ValidationManager()
    if request.method=='POST':
        request.session['errors']={}
        errors= validator.validateupdate(request.POST)
        request.session['errors']=errors
        if len(errors)>0:
            return redirect(request.POST['nextpath'])
        x=User.objects.get(id=request.session['loggedid'])
        x.first_name=request.POST['first_name']
        x.last_name=request.POST['last_name']
        x.email=request.POST['email']
        x.username=request.POST['username']
        x.save()
        return redirect('loginapp:showprofile', uid=request.POST['userid'])
    return redirect('loginapp:index')