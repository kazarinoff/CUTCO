from django.shortcuts import render, HttpResponse, redirect
from apps.loginregister.models import *
from datetime import datetime
import bcrypt
from apps.Courses.models import *

def permissionsedit(request):
    context={}
    return render(request,'permissionupdate.html',context)

def permissionsshow(request):
    x=User.objects.get(id=request.session['loggedid'])
    permissions=Permission.objects.filter(user=x)
    print('trythis',permissions)
    return render(request,'permissionsshow.html',{'user':x,'permissions':permissions})
