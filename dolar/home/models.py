from time import strftime
from django.db import models
from django.utils.timesince import timesince
from datetime import datetime

class Cotizacion(models.Model):
    datetime = models.DateTimeField()
    currency = models.CharField(max_length=50, blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    buy = models.FloatField()
    sell = models.FloatField()
    other = models.FloatField()

    def __str__(self):
        return f"{self.currency.upper()} {self.name.upper()} {datetime.strftime(self.datetime, '%Y-%m-%d %H:%M:%S')}"

    # def time_diff(self):
    #     return timesince(self.datetime, datetime.now()).split(",")[0]

    def date_month(self):
        return datetime.strftime("%m-%d", self.datetime)

    def time_relative(self):
        days = (datetime.now().date() - self.datetime.date()).days
        hours = (datetime.now().hour - self.datetime.hour)
        minutes = (datetime.now().minute - self.datetime.minute)
        if days == 0:
            # difference = 'Hoy'
            if hours == 1:
                difference = f'Hace 1 h'
            elif hours > 1:
                difference = f'Hace {hours} hs'
            else:
                difference = f'Hace {minutes} min'
        elif days == 1:
            difference = 'Ayer'
        elif days > 1:
            difference = f'Hace {days} días'
        return difference

    class Meta:
        managed = False
        db_table = 'cotizacion'
