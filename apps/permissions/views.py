from django.shortcuts import render, HttpResponse, redirect
from apps.loginregister.models import *
from datetime import datetime
import bcrypt
from apps.Courses.models import *

def permissionsedit(request):
    context={}
    return render(request,'permissionupdate.html',context)
