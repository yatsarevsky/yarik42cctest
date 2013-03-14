from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save, post_delete

from datetime import datetime


__all__ = ['VCard', 'RequestStore', 'EntryLog']


class VCard(models.Model):
    name = models.CharField(max_length=64, verbose_name='Name')
    surname = models.CharField(max_length=64, verbose_name='Surname')
    birth_date = models.DateField(verbose_name='Birth Date')
    bio = models.TextField(blank=True, verbose_name='BIO')
    e_mail = models.EmailField(verbose_name='E-mail')
    photo = models.ImageField(upload_to='photo', blank=True)
    skype = models.CharField(max_length=64, blank=True, verbose_name='Skype')
    mob = models.CharField(max_length=64, blank=True, verbose_name='Mob.')
    jid = models.CharField(max_length=64, verbose_name='JID')

    def __unicode__(self):
        return '%s %s' % (self.name, self.surname)


class RequestStore(models.Model):
    host = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.now())
    priority = models.PositiveIntegerField(default=0)

    class Meta:
            ordering = ['-priority']

    def __unicode__(self):
        return '%s %s' % (self.host, self.date)


class EntryLog(models.Model):
    ACTIONS = (
        ('0', 'Changed'),
        ('1', 'Created'),
        ('2', 'Deleted'),
    )
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    action = models.CharField(max_length=1, choices=ACTIONS)
    date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return '%s %s' % (self.content_object, self.date)


def log(sender, **kwargs):
    APP = ('vcard', 'auth', 'flatpages')
    if sender._meta.app_label in APP and sender is not EntryLog:
        action = str(int(kwargs.get('created', '2')))

        EntryLog.objects.create(content_object=kwargs['instance'],
            action=action)

post_save.connect(log)
post_delete.connect(log)
