import uuid as uuid
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.datetime_safe import datetime


class Station(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()
    importance = models.IntegerField(default=0)

    def __str__(self):
        return "Station '" + self.name + "'"


class Company(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return "Company '" + self.name + "'"


class SellPoint(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    cups_desired = models.IntegerField(default=50)
    cups_current = models.IntegerField(default=50)
    def __str__(self):
        return "SellPoint '" + self.name + "'"

    def decrement_current(self):
        self.cups_current = self.cups_current - 1
        self.save()

    def increment_current(self):
        self.cups_current = self.cups_current + 1
        self.save()


class DropOff(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    cups_current = models.IntegerField(default=50)

    def decrement_current(self):
        self.cups_current = self.cups_current - 1
        self.save()

    def increment_current(self):
        self.cups_current = self.cups_current + 1
        self.save()

class CustomUser(AbstractUser):
    role = models.IntegerField(default=1)
    sellPoint = models.ForeignKey(SellPoint,
                                  null=True,
                                  blank=True,
                                  default=None,
                                  on_delete=models.CASCADE,
                                  verbose_name="selling point (shop assistant)")
    dropOff = models.ForeignKey(DropOff,
                                  null=True,
                                  blank=True,
                                  default=None,
                                  on_delete=models.CASCADE,
                                  verbose_name="dropoff point (return machine)")
    balance = models.FloatField(default=0.0)

    def is_user(self):
        return self.role == 1

    def is_store(self):
        assert (self.sellPoint is not None)
        return self.role == 2

    def is_admin(self):
        return self.role == 999

    def increment_balance(self):
        self.balance = self.balance + 0.5
        self.save()



class Cup(models.Model):
    # Unique id
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    size = models.IntegerField(default=0)
    time1 = models.DateTimeField(null=True, default=datetime.now())
    time2 = models.DateTimeField(null=True, default=None)
    time3 = models.DateTimeField(null=True, default=None)
    time4 = models.DateTimeField(null=True, default=None)

    # Foreign Keys (can be null)
    # SellPoint shouldn't be empty while initializing!!!!!
    sellPoint = models.ForeignKey(SellPoint, on_delete=models.CASCADE, null=True)
    dropOff = models.ForeignKey(DropOff, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def sell_cup(self):
        self.time2 = datetime.now()
        self.save()

    def assign_to_user(self, user: CustomUser):
        self.user = user
        self.time3 = datetime.now()
        self.save()

        assert (self.sellPoint is not None)
        assert (self.user is not None)
        assert (self.dropOff is None)

    def return_to_dropoff(self, dropOff: DropOff):
        self.dropOff = dropOff
        self.sellPoint = None
        self.time4 = datetime.now()
        self.save()

        assert (self.user is not None)
        assert (self.dropOff is not None)

    def clean_at_dropoff(self):
        self.user = None
        self.time1 = datetime.now()
        self.save()

        assert (self.sellPoint is None)
        assert (self.user is None)
        assert (self.dropOff is not None)


class Movement(models.Model):
    origin = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="origin")
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="destination")
    quantity = models.IntegerField(default=0)
