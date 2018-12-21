from django.db import models
from apps.loginregister.models import *

class Course(models.Model):
    course_number = models.CharField(max_length=10)
    course_name = models.CharField(max_length=50)
    credits = models.FloatField()
    department = models.ForeignKey(Dept,on_delete='CASCADE', related_name='courses')
    college = models.ForeignKey(College,on_delete='CASCADE', related_name='courses')
    prereqs = models.ManyToManyField('self', related_name="requiredforcourses")
    equivalencies = models.ManyToManyField('self', related_name='equivalentcourses')
    course_description = models.TextField()
    course_outcomes = models.TextField()
    course_URL = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete='CASCADE',related_name='addedcourses')
    edited_at = models.DateTimeField(auto_now=True)
    def formatcourse(self):
        self.course_name=self.course_name.replace("_"," ")
        return self

class Degree(models.Model):
    name=models.CharField(max_length=255)
    college=models.ForeignKey(College, on_delete='cascade', related_name='degrees')
    credits = models.FloatField()
    reqcourses=models.ManyToManyField(Course, related_name='requiredfordegree')

class CourseValidator(models.Manager):    
    def validatecourse(self, postData):
        errors = {}
        if (len(postData['course_name'])<1):
            errors['course_name']='Please add a name to your course.'
        if (len(postData['course_number'])<1):
            errors['course_name']='Please include a course number.'
        if (len(postData['credits'])<1):
            errors['course_name']='Please a number of credits.'
        if (len(postData['course_description'])<10):
            errors['course_description']='Please include a longer description.'
        if (len(postData['course_outcomes'])<10):
            errors['course_outcomes']='Please include all course outcomes.'
        return errors

