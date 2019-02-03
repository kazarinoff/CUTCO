from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')
from apps.Courses.models import *

class College(models.Model):
    name=models.CharField(max_length=255)
    city=models.CharField(max_length=50)
    def formatcollege(self):
        self.name=self.name.replace("_"," ")
        return self

class Dept(models.Model):
    name=models.CharField(max_length=255)
    college=models.ForeignKey(College,on_delete='cascade',related_name='departments')

class User(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    colleges=models.ManyToManyField(College,related_name='users')
    permissions=models.ManyToManyField(Dept,through='Permission',related_name='users')
    role=models.CharField(max_length=20)
    passwordhash=models.CharField(max_length=255)
    accesslevel=models.IntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def __repr__(self):
        return ("USER: {}".format(self.first_name))

class Permission(models.Model):
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)

class ValidationManager(models.Manager):
    def validatereg(self, postData):
        errors = {}
        if (len(postData['first_name']) < 1) or (not NAME_REGEX.match(postData['first_name'])):
            errors["first_name"] = "Please enter your first name, using only letters."
        if (len(postData['last_name']) < 1) or (not NAME_REGEX.match(postData['last_name'])):
            errors["last_name"] = "Please enter your last name, using only letters."
        if (len(postData['username']) < 1):
            errors["username"] = "Please enter a username."
        if (len(User.objects.filter(username=postData['username']))>0):
            errors['username']='That username is already taken. Please enter a new one.'
        if (len(postData['email'])< 1) or (not EMAIL_REGEX.match(postData['email'])):
            errors['email'] ="Please enter a valid email address"    
        if (len(User.objects.filter(email=postData['email'])))>0:
            errors['email'] = "This email is already in database. Please reset your password if you are unable to login."
        if postData['password']!=postData['confirmpw']:
            errors['confirmpw']="Your passwords did not match. Please try again."
        if len(postData['password'])<8:
            errors['password']="Please choose a password with at least 8 characters."
        return errors
    
    def validatelogin(self, postData):
        errors = {}
        if (len(User.objects.filter(username=postData['username']))<1):
            errors['loginusername']='No user was found matching that name. Please try again.'
        else:
            x=User.objects.get(username=postData['username'])
            if not bcrypt.checkpw(postData['password'].encode('utf-8'), x.passwordhash.encode()):
                errors['loginpassword']="Your password did not match your account. Please try again."
        return errors
    
    def validateupdate(self,postData):
        errors = {}
        if (len(postData['first_name']) < 1) or (not NAME_REGEX.match(postData['first_name'])):
            errors["first_name"] = "Please enter your first name, using only letters."
        if (len(postData['last_name']) < 1) or (not NAME_REGEX.match(postData['last_name'])):
            errors["last_name"] = "Please enter your last name, using only letters."
        if (len(postData['email'])< 1) or (not EMAIL_REGEX.match(postData['email'])):
            errors['email'] ="Please enter a valid email address" 
        if (len(User.objects.filter(email=postData['email'])))>1:
            errors['email'] = "This email is already in database. Please try again."
        if (len(postData['username']) < 1):
            errors["username"] = "Please enter a username."
        if (len(User.objects.filter(username=postData['username']))>0):
            errors['username']='That username is already taken. Please enter a new one.'
        return errors