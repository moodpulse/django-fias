# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models

__all__ = ['Version', 'Status']


class VersionManager(models.Manager):

    def nearest_by_date(self, date):
        try:
            return self.get_queryset().filter(dumpdate=date).latest('dumpdate')
        except Version.DoesNotExist:
            return self.get_queryset().filter(dumpdate__lte=date).latest('dumpdate')


class Version(models.Model):

    class Meta:
        app_label = 'fias'

    objects = VersionManager()

    ver = models.IntegerField(primary_key=True)
    date = models.DateField(db_index=True, blank=True, null=True)
    dumpdate = models.DateField(db_index=True)

    complete_xml_url = models.CharField(max_length=255)
    complete_dbf_url = models.CharField(max_length=255)
    delta_xml_url = models.CharField(max_length=255, blank=True, null=True)
    delta_dbf_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{0} from {1}'.format(self.ver, self.dumpdate)


class Status(models.Model):

    class Meta:
        app_label = 'fias'

    table = models.CharField(primary_key=True, max_length=15)
    ver = models.ForeignKey(Version, on_delete=models.CASCADE)

    def __str__(self):
        return self.table
