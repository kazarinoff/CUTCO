from django.shortcuts import render, HttpResponse, redirect
from apps.loginregister.models import *
from datetime import datetime
import bcrypt
from apps.Courses.models import *

def index(request):
    if 'loggedid' in request.session:
        return redirect('/courses/')
    if 'errors' not in request.session:
        request.session['errors']={}
    context={'colleges':College.objects.all(),'departments':Dept.objects.all(),'errors':request.session['errors']}
    return render(request,'login.html',context)

def regval(request):
    validator= ValidationManager()
    if request.method=='POST':
        request.session['errors']={}
        errors= validator.validatereg(request.POST)
        if not len(errors):
            pwd=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            pwdcrpt=pwd.decode('utf-8')
            print(pwdcrpt)
            x=User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'], username=request.POST['username'], passwordhash=pwdcrpt)
            x.colleges.add(College.objects.get(name=str(request.POST['college'])))
            x.save()
            request.session['loggedid']=User.objects.last().id
            return redirect('/courses/')
        else:
            request.session['errors']=errors
            return redirect('/login/')
    return redirect('/login/')

def loginval(request):
    validator= ValidationManager()
    request.session['errors']={}
    if request.method=='POST':
        errors= validator.validatelogin(request.POST)
        if not len(errors):
            request.session['loggedid']=User.objects.get(username=request.POST['username']).id
            return redirect ('/courses/')
        else:
            request.session['errors']=errors
    return redirect('/login/')

def logout(request):
    request.session.clear()
    return redirect('/login/')

def edituser(request):
    if 'errors' not in request.session:
        request.session['errors']={}
    x=User.objects.get(id=request.session['loggedid'])
    context={'errors':request.session['errors'], 'user':x, 'admin':x.accesslevel, 'courses':Course.objects.all(), 'departments':Dept.objects.all(), 'colleges':College.objects.all()}
    return render (request,'useredit.html',context)

def updateuser(request):
    validator= ValidationManager()
    if request.method=='POST':
        request.session['errors']={}
        errors= validator.validateupdate(request.POST)
        request.session['errors']=errors
        if len(errors)>0:
            return redirect('/login/profile/')
        x=User.objects.get(id=request.session['loggedid'])
        x.first_name=request.POST['first_name']
        x.last_name=request.POST['last_name']
        x.email=request.POST['email']
        x.username=request.POST['username']
        x.save()
        return redirect('/courses/')
    return redirect('/login/')