from django.db import models


class NavData(models.Model):
    DIR_CHOICES = (
        ('N', 'North'),
        ('E', 'East'),
        ('S', 'South'),
        ('W', 'West')
    )
    time_stamp = models.CharField(max_length=32, verbose_name='Время замера', blank=True)
    latitude = models.CharField(max_length=32, verbose_name='Широта', blank=True)
    lat_direction = models.CharField(max_length=2, choices=DIR_CHOICES, blank=True)
    longitude = models.CharField(max_length=32, verbose_name='Долгота', blank=True)
    long_direction = models.CharField(max_length=2, choices=DIR_CHOICES, blank=True)
    altitude = models.CharField(max_length=32, blank=True)
    speed = models.CharField(max_length=32, blank=True)


    @property
    def get_time_humanized(self):
        hours = self.time_stamp[:2]
        minutes = self.time_stamp[2:4]
        seconds = self.time_stamp[4:]
        return str(hours) + ' ч. ' + str(minutes) + ' мин. ' + str(seconds) + ' c'

    @property
    def get_latitude_humanized(self):
        grad = self.latitude[:2]
        minutes = self.latitude[2:]

        if self.lat_direction == 'N':
            return str(self.latitude) + ' северной широты'




