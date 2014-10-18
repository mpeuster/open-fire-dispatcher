from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=128)
    name2 = models.CharField(max_length=128, blank=True)
    sms_gateway_driver = models.IntegerField(default=0)
    sms_gateway_sender = models.IntegerField(default=112112112)
    sms_gateway_api_key = models.CharField(max_length=256, blank=True)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class DepartmentManager(models.Model):
    user = models.OneToOneField(User)
    department = models.ForeignKey(Department)

    def __unicode__(self):
        return str(self.user)


class Contact(models.Model):
    department = models.ForeignKey(Department)
    name = models.CharField(max_length=128)
    mail1 = models.EmailField(blank=True)
    mail2 = models.EmailField(blank=True)
    sms1 = models.IntegerField(default=0)
    sms2 = models.IntegerField(default=0)
    test = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class AlarmLoop(models.Model):
    department = models.ForeignKey(Department)
    contacts = models.ManyToManyField(Contact, blank=True)
    loop = models.CharField(max_length=5, default="00000")
    alarm_text = models.CharField(max_length=140,
                                  default="Feuerwehr Alarmierung!")
    alarm_text_long = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.loop


class Alarm(models.Model):
    loop = models.ForeignKey(AlarmLoop)
    alarm_time = models.DateTimeField(auto_now_add=True)
    alarm_message = models.TextField(blank=False)

    def __unicode__(self):
        return "Alarm (%s)" % str(self.alarm_time)
