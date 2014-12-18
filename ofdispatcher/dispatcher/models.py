import logging
from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class Department(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=128)
    name2 = models.CharField(max_length=128, blank=True)
    sms_gateway_driver = models.IntegerField(default=0)
    sms_gateway_sender = models.IntegerField(default=112112112)
    sms_gateway_api_key = models.CharField(max_length=256, blank=True)
    comment = models.TextField(blank=True)  # hidden comment
    news = models.TextField(blank=True)  # public notification

    def __unicode__(self):
        return self.name


class DepartmentManager(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User)
    department = models.ForeignKey(Department)

    def __unicode__(self):
        return '%s-%s' % (str(self.user), str(self.department))


class Contact(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    department = models.ForeignKey(Department)
    firstname = models.CharField(max_length=128)
    secondname = models.CharField(max_length=128)
    mail1 = models.EmailField(blank=True)
    mail2 = models.EmailField(blank=True)
    sms1 = models.IntegerField(default=0)
    sms2 = models.IntegerField(default=0)
    test = models.BooleanField(default=True)
    error = models.BooleanField(default=False)
    dev = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s, %s' % (self.secondname, self.firstname)

    def update_alarmloop_assignment(self, loops):
        '''
        Add this user to all AlarmLoops which are specified
        in the loops list. The list has to contain
        AlarmLoop ids.
        '''
        # remove this contact from all loops
        for al in AlarmLoop.objects.all():
            al.contacts.remove(self)
        # re-assign contact to loop(s) specified in list
        loop_list = []
        for loop_id in loops:
            al = AlarmLoop.objects.get(id=int(loop_id))
            loop_list.append(al)
            al.contacts.add(self)
        logger.info('Contact %s assigned to loops: %s', self, loop_list)
        return loop_list

    def get_alarmloop_assignment(self):
        '''
        Returns list of AlarmLoops that to which this contact
        is currently assigned.
        '''
        return [l for l in AlarmLoop.objects.filter(contacts=self)]


class AlarmLoop(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    department = models.ForeignKey(Department)
    contacts = models.ManyToManyField(Contact, blank=True)
    loop = models.CharField(max_length=5, default='00000')
    name = models.CharField(max_length=128, default='Schleife')
    alarm_text = models.CharField(max_length=140,
                                  default='Feuerwehr Alarmierung!')
    alarm_text_long = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    # definition of test alarm times for this loop
    test_alarm_day = models.IntegerField(default=5)  # Mo=0,...
    test_alarm_date_min = models.IntegerField(default=1)  # e.g. 1
    test_alarm_date_max = models.IntegerField(default=7)  # e.g. 7
    test_alarm_hour = models.IntegerField(default=12)  # start hour
    test_alarm_minute = models.IntegerField(default=10)  # start minute
    test_alarm_period = models.IntegerField(default=30)  # test period

    def __unicode__(self):
        return self.loop


class Alarm(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    loop = models.ForeignKey(AlarmLoop)
    message = models.TextField(blank=False)
    log = models.TextField(blank=True)
    type = models.IntegerField(default=0)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        return 'Alarm (%s)' % str(self.created)
