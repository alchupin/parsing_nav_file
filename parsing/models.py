from django.db import models


class NavData(models.Model):
    time_stamp = models.CharField(max_length=32, verbose_name='Время замера', blank=True)

    latitude_degrees = models.CharField(max_length=32, verbose_name='Широта, градусы', blank=True)
    latitude_minutes = models.CharField(max_length=32, verbose_name='Широта, минуты', blank=True)
    latitude_dir = models.CharField(max_length=2, blank=True)

    longitude_degrees = models.CharField(max_length=32, verbose_name='Долгота, градусы', blank=True)
    longitude_minutes = models.CharField(max_length=32, verbose_name='Долгота, минуты', blank=True)
    longitude_dir = models.CharField(max_length=2, blank=True)

    altitude = models.DecimalField(max_digits=8, decimal_places=1, verbose_name='Высота над уровнем моря, м', blank=True)
    speed = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Скорость, узлы', blank=True)

    @property
    def get_time_humanized(self):
        """
        Возвращает время в человекочитаемом виде
        """
        hours = self.time_stamp[:2]
        minutes = self.time_stamp[2:4]
        seconds = self.time_stamp[4:]

        return str(hours) + ' ч. ' + str(minutes) + ' мин. ' + str(seconds) + ' c'

    @property
    def get_coordinates(self):
        """
        Возвращает координаты в человекочитаемом виде
        """
        degree = '\u00b0'

        return self.latitude_degrees + degree + self.latitude_minutes + '\'' + self.latitude_dir +\
               self.longitude_degrees + degree + self.longitude_minutes + '\'' + self.longitude_dir




