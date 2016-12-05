from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class SensorType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name;


class SensorDetail(models.Model):
    sensor_id = models.CharField(max_length=100)
    station_name = models.CharField(max_length=400)
    station_desc = models.CharField(max_length=800)
    sensor_type = models.ForeignKey(SensorType)
    latitude = models.FloatField(max_length=10)
    longitude = models.FloatField(max_length=10)
    location = models.CharField(max_length=400)
    active = models.BooleanField(default=True)
    sensorOwner = models.ForeignKey(User, on_delete=models.CASCADE)
    container_id = models.CharField(max_length=100, default='0')

    def __str__(self):
        return self.station_name+''


class UserSensorDetail(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    sensor_id = models.ForeignKey(SensorDetail, on_delete=models.CASCADE)

