from django.shortcuts import render, HttpResponse, redirect
from apps.loginregister.models import *
from apps.Courses.models import *
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

def home(request):
    x={}
    xp=[]
    if 'loggedid' in request.session:
        x=User.objects.get(id=request.session['loggedid'])
        xp=Permission.objects.filter(user=x)
    c=College.objects.values('name','departments__name','departments__courses__course_name','departments__courses__course_number','departments__courses__credits','departments__courses__id','departments__courses__prereqs__course_number')
    alldepts=Dept.objects.all()
    return render (request,'courseshome.html',{'allcourses':c,'user':x,'permissions':xp})

def viewcourse(request,idnumber):
    x={}
    if 'loggedid' in request.session:
        x=User.objects.get(id=request.session['loggedid'])
    y=Course.objects.get(id=idnumber)
    z=y.prereqs.all()
    w=y.equivalencies.all()
    return render (request,'courseinfo.html',{'user':x,'course':y, 'prereqs':z, 'equivalencies':w})

def addcourseform(request):
    if 'loggedid' not in request.session:
        return redirect('/login/')
    x=User.objects.get(id=request.session['loggedid'])
    d=Permission.objects.filter(user=x,level__gt=2).values('dept__name','dept__college__name','dept_id')
    errors=request.session['errors']
    context={'user':x,'availdepts':d,'prereqs':Course.objects.all(),'errors':errors}
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
            p=False
        if not p:
            return HttpResponse('You are not important enough to create a course in this department')
        else:
            validator=CourseValidator()
            errors=validator.validatecourse(request.POST)
            if len(errors)>0:
                request.session['errors']=errors
                return redirect(reqest.POST['newpath'])
            else:
                y=Course.objects.create(college=y.college, department=y,created_by=x,course_name=request.POST['course_name'],course_number=request.POST['course_number'],credits=request.POST['credits'],course_description=request.POST['course_description'],course_outcomes=request.POST['course_outcomes'],course_URL=request.POST['course_url'])
                y.save()
                return redirect('/courses/')

def editcourse(request,idnumber):
    if 'loggedid' not in request.session:
        return redirect('/login/')
    x=User.objects.get(id=request.session['loggedid'])
    y=Course.objects.get(id=idnumber)
    try:
        p=Permission.objects.get(user=x,dept=y.department)
    except ObjectDoesNotExist:
        p=False
    if not p:
        return HttpResponse('YOU ARE NOT ALLOWED TO ACCESS THIS AREA.')
    else:
        if p.level>=2:
            return render(request,'editcourse.html',{'user':x,"course":y, "prereqsselected":y.prereqs.all(), "prereqsother":Course.objects.filter(college=y.college).exclude(id=y.id)})
        else:
            return HttpResponse('YOU ARE NOT ALLOWED TO ACCESS THIS AREA.')
def updatecourse(request,idnumber):
    if request.method=='POST':
        if 'loggedid' not in request.session:
            return redirect('/login/')
        x=User.objects.get(id=request.session['loggedid'])
        request.session['errors']={}
        validator=CourseValidator()
        errors=validator.validatecourse(request.POST)
        if len(errors)>0:
            return redirect('/courses/<idnumber>/edit/')
        y=Course.objects.get(id=int(idnumber))
        yr=y.prereqs.all()
        for h in yr:
            y.prereqs.remove(h)
        y.course_name=request.POST['course_name']
        y.course_number=request.POST['course_number']
        y.credits=request.POST['credits']
        z=request.POST.getlist('prereqs')
        for item in z:
            y.prereqs.add(Course.objects.get(id=str(item)))
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
    y=Course.objects.get(id=idnumber)
    try:
        p=Permission.objects.get(user=x,dept=y.department)
    except ObjectDoesNotExist:
        p=False
    if not p:
        return HttpResponse('YOU ARE NOT ALLOWED TO DELETE THIS COURSE.')
    else:
        if p.level>=5:
            return render(request,'deletecourse.html', {'user':x,'course':y})
        else:
            return HttpResponse("Please talk to your administrator to get this course deleted")
def deletecourse(request,idnumber):
    if 'loggedid' not in request.session:
        return redirect('/login/')
    if request.method=='POST':
        x=User.objects.get(id=request.session['loggedid'])
        y=Course.objects.get(id=idnumber)
        try:
            p=Permission.objects.get(user=x,dept=y.department)
        except ObjectDoesNotExist:
            p=False
        if not p:
            return HttpResponse('YOU ARE NOT ALLOWED TO DELETE THIS COURSE.')
        y.delete()
    return redirect('/courses/')

def viewtreq(request,idnumber):
    x={}
    if 'loggedid' not in request.session:
        return redirect('/login/')
    x=User.objects.get(id=request.session['loggedid'])
    y=Course.objects.get(id=idnumber)
    dptmt=Dept.objects.exclude(college=y.college)
    z=Course.objects.exclude(college=y.college).order_by('college','department','course_number')
    return render(request,'edittreq.html',{'user':x,'course':y,'availdepts':dptmt, 'availcourses':z})

def edittreq(request,idnumber):
    if 'loggedid' not in request.session:
        return redirect('/login/')
    x=User.objects.get(id=request.session['loggedid'])
    y=Course.objects.get(id=idnumber)
    if request.method =='POST':
        try:
            p=Permission.objects.get(user=x,dept=y.department)
        except ObjectDoesNotExist:
            p=False
        if not p:
            return HttpResponse('YOU ARE NOT ALLOWED TO MODIFY EQUIVALENCIES FOR THIS COURSE.')
        ye= y.equivalencies.filter(department=request.POST['deptid'])
        for h in ye:
            y.equivalencies.remove(h)
        z=request.POST.getlist('equivalency')
        for item in z:
            y.equivalencies.add(Course.objects.get(id=str(item)))
        y.save()
        return redirect('/courses/'+idnumber)
    return redirect ('/courses/')

def treqtable(request):
    x={}
    if 'loggedid' not in request.session:
        pass
    else:
        x=User.objects.get(id=request.session['loggedid'])
    if 'treqtablecollegeid1' not in request.session:
        y=College.objects.first()
    else:
        y=College.objects.get(id=request.session['treqtablecollegeid1'])
    if 'treqtablecollegeid2' not in request.session:
        z=College.objects.last()
    else:
        z=College.objects.get(id=request.session['treqtablecollegeid2'])
    courseinfo=y.courses.values('course_name','equivalencies__course_name','course_number','id','equivalencies__course_number','equivalencies__id').filter(Q(equivalencies__college=z) | Q(equivalencies__isnull=True)).order_by('course_number')
    return render(request,'treqtable.html',{'colleges':College.objects.all(),'user':x, 'yourcollege':y.formatcollege,'othercollege':z.formatcollege,'yourcollegecourses':courseinfo})

def treqtablegenerate(request):
    if request.method=='POST':
        request.session['treqtablecollegeid1']=request.POST['yourcollegeid']
        request.session['treqtablecollegeid2']=request.POST['othercollegeid']
    return redirect ('/courses/treqtable/')