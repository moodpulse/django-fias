#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models

from fias.fields import UUIDField
from fias.models.house import House
from fias.models.status import OperStat

__all__ = ['Room', 'FlatType', 'RoomType']


class AbstractType(models.Model):
    name = models.CharField('Наименование типа', max_length=255)
    shortname = models.CharField('Краткое наименование типа', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class FlatType(AbstractType):
    """
    Классификатор типов помещения или офиса
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Тип помещения или офиса'
        verbose_name_plural = 'Типы помещения или офиса'

    fltypeid = models.PositiveIntegerField('Идентификатор типа помещения или офиса', primary_key=True)


class RoomType(AbstractType):
    """
    Классификатор типов комнат
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Тип комнаты'
        verbose_name_plural = 'Типы комнат'

    rmtypeid = models.PositiveIntegerField('Идентификатор типа комнаты', primary_key=True)


class Room(models.Model):
    """
    Классификатор помещений
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'

    houseguid = models.ForeignKey(House, verbose_name='Идентификатор родительского объекта (дома)', on_delete=models.CASCADE)
    roomguid = UUIDField('Глобальный уникальный идентификатор адресного объекта (помещения)', primary_key=True)
    roomid = UUIDField('Уникальный идентификатор записи.', unique=True)
    previd = UUIDField('Идентификатор записи связывания с предыдушей исторической записью', blank=True, null=True)
    nextid = UUIDField('Идентификатор записи  связывания с последующей исторической записью', blank=True, null=True)
    flatnumber = models.CharField('Номер помещения или офиса', max_length=50)
    flattype = models.IntegerField('Тип помещения')
    roomnumber = models.CharField('Номер комнаты', max_length=50, blank=True, null=True)
    roomtype = models.IntegerField('Тип комнаты', blank=True, null=True)
    regioncode = models.CharField('Код региона', max_length=2)
    postalcode = models.PositiveIntegerField('Почтовый индекс', blank=True, null=True)
    updatedate = models.DateField('Дата  внесения записи')

    startdate = models.DateField('Начало действия записи')
    enddate = models.DateField('Окончание действия записи')

    livestatus = models.BooleanField('Признак действующего адресного объекта', default=False)

    normdoc = UUIDField('Внешний ключ на нормативный документ', blank=True, null=True)

    operstatus = models.ForeignKey(OperStat, verbose_name='Статус действия над записью – причина появления записи',
                                   default=0, on_delete=models.CASCADE)

    cadnum = models.CharField('Кадастровый номер помещения', max_length=100, blank=True, null=True)
    roomcadnum = models.CharField('Кадастровый номер комнаты в помещении', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.flatnumber
