from django.db import models

from datetime import datetime


__all__ = ['VCard', 'RequestStore']


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

    def __unicode__(self):
        return '%s %s' % (self.host, self.date)
