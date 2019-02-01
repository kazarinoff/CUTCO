from django.shortcuts import render, HttpResponse, redirect
from apps.loginregister.models import *
from apps.Courses.models import *
from datetime import datetime

def home(request):
    if 'loggedid' not in request.session:
        return redirect('/login/')
    else:
        x=User.objects.get(id=request.session['loggedid'])
        courses=Course.objects.all().order_by('college','department','course_number')
        courseinfo=[]
        for z in courses:
            print(z,'print?')
            pqs=[]
            for k in z.prereqs.all():
                pqs.append(k)
            courseinfo.append({'course_name':z.course_name,'course_number':z.course_number, 'id':z.id,'prereqs':pqs,'credits':z.credits})
        context={'user':x, 'admin':x.accesslevel, 'courses':courseinfo, 'departments':Dept.objects.all(), 'colleges':College.objects.all()}
        return render (request,'courseshome.html',context)

def viewcourse(request,idnumber):
    x=User.objects.get(id=request.session['loggedid'])
    y=Course.objects.get(id=idnumber)
    z=y.prereqs.all()
    w=y.equivalencies.all()
    return render (request,'courseinfo.html',{'user':x,'course':y, 'prereqs':z, 'equivalencies':w})

def addcourseform(request):
    x=User.objects.get(id=request.session['loggedid'])
    d=x.departments.all()
    if x.accesslevel<7:
        return HttpResponse('YOU ARE NOT ALLOWED TO ACCESS THIS AREA')
    errors=request.session['errors']
    context={'user':x,'availdepts':d,'prereqs':Course.objects.all(),'errors':errors}
    return render(request,'addcourse.html',context)


def addcourse(request):
    if request.method=='POST':
        x=User.objects.get(id=request.session['loggedid'])
        if x.accesslevel<7:
            return HttpResponse('YOU ARE NOT ALLOWED TO ACCESS THIS AREA')
        else:
            validator=CourseValidator()
            errors=validator.validatecourse(request.POST)
            if len(errors)>0:
                request.session['errors']=errors
                return redirect('/courses/add')
            else:
                z=Dept.objects.get(id=request.POST['deptid'])
                y=Course.objects.create(college=z.college, department=z,created_by=x,course_name=request.POST['course_name'],course_number=request.POST['course_number'],credits=request.POST['credits'],course_description=request.POST['course_description'],course_outcomes=request.POST['course_outcomes'],course_URL=request.POST['course_url'])
                y.save()
                return redirect('/courses/')

def editcourse(request,idnumber):
    x=User.objects.get(id=request.session['loggedid'])
    y=Course.objects.get(id=idnumber)
    if x.accesslevel < 7:
        return HttpResponse('YOU ARE NOT ALLOWED TO ACCESS THIS AREA. YOU ARE NOT  A 7')
    if  y.department not in x.departments.all():
        return HttpResponse('YOU ARE NOT ALLOWED TO ACCESS THIS AREA')
    else:
        return render(request,'editcourse.html',{'user':x,"course":y, "prereqsselected":y.prereqs.all(), "prereqsother":Course.objects.filter(college=y.college).exclude(id=y.id)})

def updatecourse(request,idnumber):
    if request.method=='POST':
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
    x=User.objects.get(id=request.session['loggedid'])
    y=Course.objects.get(id=idnumber)
    if x.accesslevel < 7:
        return HttpResponse('YOU ARE NOT ALLOWED TO DELETE THIS COURSE. YOU ARE NOT A 7')
    if  y.department not in x.departments.all():
        return HttpResponse('YOU ARE NOT ALLOWED TO DELETE THIS COURSE. IT AINT YOUR DEPARTMENT!')
    return render(request,'deletecourse.html', {'user':x,'course':y})

def deletecourse(request,idnumber):
    if request.method=='POST':
        x=User.objects.get(id=request.session['loggedid'])
        y=Course.objects.get(id=idnumber)
        if x.accesslevel < 7:
            return HttpResponse('YOU ARE NOT ALLOWED TO DELETE THIS COURSE. YOU ARE NOT A 7')
        if  y.department not in x.departments.all():
            return HttpResponse('YOU ARE NOT ALLOWED TO DELETE THIS COURSE. IT AINT YOUR DEPARTMENT!')
        y.delete()
    return redirect('/courses/')

def viewtreq(request,idnumber):
    x=User.objects.get(id=request.session['loggedid'])
    y=Course.objects.get(id=idnumber)
    dptmt=Dept.objects.exclude(college=y.college)
    z=Course.objects.exclude(college=y.college).order_by('college','department','course_number')
    return render(request,'edittreq.html',{'user':x,'course':y,'availdepts':dptmt, 'availcourses':z})

def edittreq(request,idnumber):
    x=User.objects.get(id=request.session['loggedid'])
    y=Course.objects.get(id=idnumber)
    print('gotHERE!!!!!!!!!!!!!!!!!!')
    if request.method =='POST':
        if x.accesslevel < 7:
            return HttpResponse('YOU ARE NOT ALLOWED TO MODIFY EQUIVALENCIES FOR THIS COURSE. YOU ARE NOT A 7')
        if  y.department not in x.departments.all():
            return HttpResponse('YOU ARE NOT ALLOWED TO MODIFY EQUIVALENCIES FOR THIS COURSE. IT AINT YOUR DEPARTMENT!')
        ye= y.equivalencies.filter(department=request.POST['deptid'])
        print(ye,'$$$$$$$$')
        for h in ye:
            y.equivalencies.remove(h)
        z=request.POST.getlist('equivalency')
        for item in z:
            y.equivalencies.add(Course.objects.get(id=str(item)))
        y.save()
        print(y.equivalencies.all(),'******************')
        return redirect('/courses/'+idnumber)
    return redirect ('/courses/')

def treqtable(request):
    x=User.objects.get(id=request.session['loggedid'])
    if 'treqtablecollegeid1' not in request.session:
        yourcollege=College.objects.first()
    else:
        yourcollege=College.objects.get(id=request.session['treqtablecollegeid1'])
    if 'treqtablecollegeid2' not in request.session:
        othercollege=College.objects.last()
        othercollegeid=othercollege.id
    else:
        othercollege=College.objects.get(id=request.session['treqtablecollegeid2'])
    courses=yourcollege.courses.all().order_by('course_number')
    courseinfo=[]
    for i in courses:
        equils=[]
        for k in i.equivalencies.filter(college=othercollege):
            equils.append(k)
        courseinfo.append({'course_name':i.course_name,'id':i.id,'course_number':i.course_number,'equilcourses':equils})
    return render(request,'treqtable.html',{'colleges':College.objects.all(),'user':x, 'yourcollege':yourcollege.formatcollege,'othercollege':othercollege.formatcollege,'yourcollegecourses':courseinfo})

def treqtablegenerate(request):
    if request.method=='POST':
        request.session['treqtablecollegeid1']=request.POST['yourcollegeid']
        request.session['treqtablecollegeid2']=request.POST['othercollegeid']
    return redirect ('/courses/treqtable/')

        
        






    




