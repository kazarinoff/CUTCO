from django.shortcuts import render, HttpResponse, redirect
from apps.loginregister.models import *
from apps.Courses.models import *
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

def home(request):
    x,xc,xd={},{},{}
    p={'god':[],'administrator':[],'faculty':[],'any':[]}
    if 'loggedid' in request.session:
        x=User.objects.get(id=request.session['loggedid'])
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
    c=College.objects.values('name','departments__name','departments__id','departments__name','departments__courses__course_name','departments__courses__course_number','departments__courses__credits','departments__courses__id','departments__courses__prereqs__course_number')
    return render (request,'courseshome.html',{'allcourses':c,'user':x,'permissions':p})

def viewcourse(request,idnumber):
    x,p,xc,xd ={},{},{},{}
    y=Course.objects.get(id=idnumber)
    if 'loggedid' in request.session:
        x=User.objects.get(id=request.session['loggedid'])
        xc=College.objects.filter(users=x)
        xd=Dept.objects.filter(users=x)
        try:
            p=Permission.objects.get(user=x,dept=y.department)
        except ObjectDoesNotExist:
            pass
    z=y.prereqs.all()
    w=y.equivalencies.all()
    return render (request,'courseinfo.html',{'usercolleges':xc,'userdepts':xd,'user':x,'course':y, 'prereqs':z, 'equivalencies':w,'permission':p, 'usercolleges':xc,'userdepts':xd})

def addcourseform(request,cid):
    if 'loggedid' not in request.session:
        return redirect('/login/')
    x=User.objects.get(id=request.session['loggedid'])
    xc=College.objects.filter(users=x)
    xd=Dept.objects.filter(users=x)
    c=College.objects.get(id=cid)
    p=Permission.objects.filter(user=x,level__gt=2,dept__college=c).values('dept__name','dept_id')
    if len(p) == 0:
        return HttpResponse('You cannot add courses to this institutions catalog')
    errors=request.session['errors']
    context={'user':x,'depts':p,'prereqs':Course.objects.filter(college=c),'errors':errors,'college':c,'usercolleges':xc,'userdepts':xd}
    return render(request,'addcourse.html',context)

def addcourse(request):
    if request.method=='POST':
        if 'loggedid' not in request.session:
            return redirect('/login/')
        x=User.objects.get(id=request.session['loggedid'])
        y=Dept.objects.get(id=request.POST['deptid'])        
        try:
            p=Permission.objects.get(user=x,dept=y)
        except ObjectDoesNotExist:
            return HttpResponse('You are not important enough to create a course in this department')
        
        validator=CourseValidator()
        errors=validator.validatecourse(request.POST)
        if len(errors)>0:
            request.session['errors']=errors
            return redirect(reqest.POST['newpath'])
        y=Course.objects.create(college=y.college, department=y,created_by=x,course_name=request.POST['course_name'],course_number=request.POST['course_number'],credits=request.POST['credits'],course_description=request.POST['course_description'],course_outcomes=request.POST['course_outcomes'],course_URL=request.POST['course_url'])
        y.save()
    return redirect('/courses/')

def editcourse(request,idnumber):
    if 'loggedid' not in request.session:
        return redirect('/login/')
    x=User.objects.get(id=request.session['loggedid'])
    y=Course.objects.get(id=idnumber)
    xc=College.objects.filter(users=x)
    xd=Dept.objects.filter(users=x)
    try:
        p=Permission.objects.get(user=x,dept=y.department)
    except ObjectDoesNotExist:
        return HttpResponse('YOU ARE NOT ALLOWED TO ACCESS THIS AREA.')
    if p.level < 2:
        return HttpResponse('YOU ARE NOT ALLOWED TO ACCESS THIS AREA.')
    return render(request,'editcourse.html',{'usercolleges':xc,'userdepts':xd,'user':x,"course":y, "prereqsselected":y.prereqs.all(), "prereqsother":Course.objects.filter(college=y.college).exclude(id=y.id)})

def updatecourse(request,idnumber):
    if request.method=='POST':
        if 'loggedid' not in request.session:
            return redirect('/login/')
        request.session['errors']={}
        validator=CourseValidator()
        errors=validator.validatecourse(request.POST)
        if len(errors)>0:
            return redirect('/courses/<idnumber>/edit/')
        y=Course.objects.get(id=int(idnumber))
        for h in y.prereqs.all():
            y.prereqs.remove(h)
        for course in request.POST.getlist('prereqs'):
            y.prereqs.add(Course.objects.get(id=str(course)))
        y.course_name=request.POST['course_name']
        y.course_number=request.POST['course_number']
        y.credits=request.POST['credits']
        y.course_description=request.POST['course_description']
        y.course_outcomes=request.POST['course_outcomes']
        y.course_url=request.POST['course_url']
        y.updated_at=datetime.now()
        y.save()
    return redirect('/courses/')

def deletecheck(request,idnumber):
    if 'loggedid' not in request.session:
        return redirect('/login/')
    x=User.objects.get(id=request.session['loggedid'])
    xc=College.objects.filter(users=x)
    xd=Dept.objects.filter(users=x)
    y=Course.objects.get(id=idnumber)
    try:
        p=Permission.objects.get(user=x,dept=y.department,level__gt=7)
    except ObjectDoesNotExist:
        return HttpResponse('YOU ARE NOT ALLOWED TO DELETE THIS COURSE.')
    return render(request,'deletecourse.html', {'usercolleges':xc,'userdepts':xd,'user':x,'course':y})

def deletecourse(request,idnumber):
    if 'loggedid' not in request.session:
        return redirect('/login/')
    if request.method=='POST':
        x=User.objects.get(id=request.session['loggedid'])
        y=Course.objects.get(id=idnumber)
        try:
            p=Permission.objects.get(user=x,dept=y.department,level__gt=7)
        except ObjectDoesNotExist:
            return HttpResponse('YOU ARE NOT ALLOWED TO DELETE THIS COURSE.')
        y.delete()
    return redirect('/courses/')

def viewtreq(request,idnumber):
    if 'loggedid' not in request.session:
        return redirect('/login/')
    x=User.objects.get(id=request.session['loggedid'])
    xc=College.objects.filter(users=x)
    xd=Dept.objects.filter(users=x)
    y=Course.objects.get(id=idnumber)
    try:
        p=Permission.objects.get(user=x,dept=y.department)
    except ObjectDoesNotExist:
        return HttpResponse('YOU ARE NOT ALLOWED TO CHANGE THIS COURSE.')
    z=Course.objects.exclude(college=y.college).order_by('college','department','course_number','course_name','id')
    return render(request,'edittreq.html',{'usercolleges':xc,'userdepts':xd,'user':x,'course':y,'allcourses':z})

def edittreq(request,idnumber):
    if 'loggedid' not in request.session:
        return redirect('/login/')
    x=User.objects.get(id=request.session['loggedid'])
    y=Course.objects.get(id=idnumber)
    if request.method =='POST':
        try:
            p=Permission.objects.get(user=x,dept=y.department,level__gt=7)
        except ObjectDoesNotExist:
            return HttpResponse('YOU ARE NOT ALLOWED TO MODIFY EQUIVALENCIES FOR THIS COURSE.')
        for h in y.equivalencies.filter(department=request.POST['collegeid']):
            y.equivalencies.remove(h)
        for item in request.POST.getlist('courseequils'):
            y.equivalencies.add(Course.objects.get(id=str(item)))
        y.save()
        return redirect('/courses/'+idnumber)
    return redirect ('/courses/')

def treqtable(request):
    x,xc,xd={},{},{}
    if 'loggedid' in request.session:
        x=User.objects.get(id=request.session['loggedid'])
        xc=College.objects.filter(users=x)
        xd=Dept.objects.filter(users=x)
    if 'treqtablecollegeid1' not in request.session:
        y=College.objects.first()
    else:
        y=College.objects.get(id=request.session['treqtablecollegeid1'])
    if 'treqtablecollegeid2' not in request.session:
        z=College.objects.last()
    else:
        z=College.objects.get(id=request.session['treqtablecollegeid2'])
    courseinfo=y.courses.values('course_name','equivalencies__course_name','course_number','id','equivalencies__course_number','equivalencies__id').filter(Q(equivalencies__college=z) | Q(equivalencies__isnull=True)).order_by('course_number')
    return render(request,'treqtable.html',{'usercolleges':xc,'userdepts':xd,'colleges':College.objects.all(),'user':x, 'yourcollege':y.formatcollege,'othercollege':z.formatcollege,'yourcollegecourses':courseinfo})

def treqtablegenerate(request):
    if request.method=='POST':
        request.session['treqtablecollegeid1']=request.POST['yourcollegeid']
        request.session['treqtablecollegeid2']=request.POST['othercollegeid']
    return redirect ('/courses/treqtable/')