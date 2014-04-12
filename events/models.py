from django.db import models
from django.contrib import admin

class Feed(models.Model):
    gid = models.CharField(max_length=200,primary_key=True)
    sname = models.CharField(max_length=200)
    gname = models.CharField(max_length=200)
    gstatus = models.CharField(max_length=200)
    gutime = models.DateTimeField(auto_now=True)


class Event(models.Model):
    event_id=models.BigIntegerField(primary_key=True)
    created_time=models.DateTimeField(auto_now=True)
    owner_name=models.CharField(max_length=40)
    owner_id=models.BigIntegerField()
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=10000)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    is_date_only=models.IntegerField()
    location=models.CharField(max_length=200)
    latitude=models.FloatField()
    longitude=models.FloatField()
    venue_id=models.BigIntegerField()
    state=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    street=models.CharField(max_length=200)
    zipcode=models.IntegerField()
    is_active=models.IntegerField()
