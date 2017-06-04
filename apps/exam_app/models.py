from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
from django.utils import timezone
import bcrypt
import re
NAME_REGEX =re.compile('^[A-z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserValidation(models.Manager):
    # validate data obtained from register form
    def register(self,postdata):
        errors =[]


        if len(postdata['name']) <2:
            errors.append("User name must be at least 2 characters")
        elif not NAME_REGEX.match(postdata['name']):
            errors.append("User name must only contain alphabet")


        if not EMAIL_REGEX.match(postdata['email']):
            errors.append('Email format is incorrect')
        #
        if len(postdata['password']) < 8:
            errors.append('Password must be at least 8 characters')
        elif postdata["password"] != postdata['confirmpassword']:
            errors.append('Password do not match')

        if postdata["date_birth"] == "" or len(postdata["date_birth"]) < 1:
            errors.append("Date field can not be empty")
        elif postdata["date_birth"] >= unicode(date.today()):
            errors.append("You can't be born in the future!")


        if len(errors) == 0:
            # generate new salt
            salt = bcrypt.gensalt()
            # encode the password obtained from form
            password = postdata['password'].encode()
            # hash password and salt together
            hashed_pw = bcrypt.hashpw(password, salt)
            # add the new users to database
            User.objects.create(name=postdata['name'], email= postdata['email'], password=hashed_pw, date_birth = postdata['date_birth'])
            print User.objects.all()
        return errors
    def login(self,postdata):
        errors=[]
        # check if the email in the database or not
        print User.objects.filter(email=postdata['email'])
        if User.objects.filter(email=postdata['email']):
            # encode the password to a specific format since the about email is registered
            form_pw = postdata['password'].encode()
            # encode the registered user's password fro database to a specific format
            db_pw = User.objects.get(email=postdata['email']).password.encode()
            # compare the password with the password in database
            if not bcrypt.checkpw(form_pw, db_pw):
                errors.append('Incorrect password')

        else:
            errors.append("User name has not been registered")
        return errors

class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    date_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # secrets_liked - this is a method on user object that is available through the related name

    objects = UserValidation()

    def __unicode__(self):
        return "user_id: " + str(self.id) + ", name: " + self.name + ", date_birth: " + str(self.date_birth)


class appointManager(models.Manager):
    def appointval(self, postdata, id):
        errors = []
        # print str(datetime.today()).split()[1]-> to see just the time in datetime
        print datetime.now().strftime("%H:%M")
        if not postdata['date']:
            errors.append("Date, time, and task can not be empty!")
        elif postdata['date']:
            if not postdata["date"] >= unicode(date.today()):
                errors.append("Date must be set in future!")
            if len(postdata["date"]) < 1:
                errors.append("Date field can not be empty")
            print "got to appointment post Data:", postdata['date']
        if len(Appointment.objects.filter(date = postdata['date'] ,time= postdata['time'])) > 0:
            errors.append("Can Not create an appointment on existing date and time")
        if len(postdata['task'])<2:
            errors.append("Please insert take, must be more than 2 characters")
        if len(errors)==0:
            makeappoint= Appointment.objects.create(user=User.objects.get(id=id), task= postdata['task'],date= str(postdata['date']),time= postdata['time'])
            print ("ELVA!!!!!!")
            return(True, makeappoint)
        else:
            return(False, errors)

    def edit_appointment(self, postdata, app_id):
        errors = []
        print errors
        # if postdata['edit_date']:
        if not postdata["edit_date"] >= unicode(date.today()):
            errors.append("Appointment date can't be in the past!")
            print "appoint date can't be past"
        if postdata["edit_date"] == "" or len(postdata["edit_tasks"]) < 1:
            errors.append("All fields must be filled out!")
            print "all fields must fill out pop out"
        if errors == []:
            update_time= self.filter(id = app_id).update(task = postdata['edit_tasks'], status = postdata['edit_status'], time = postdata['edit_time'], date = postdata['edit_date'])

            return (True, update_time)
        else:
            return (False, errors)

class Appointment(models.Model):
    user= models.ForeignKey(User, related_name="onrecord", blank=True, null=True)
    task= models.CharField(max_length=255)
    status= models.CharField(max_length=255)
    date= models.DateField(blank=True, null=True);
    time= models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    objects= appointManager()
