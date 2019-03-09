import uuid as uuid
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


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
    def __str__(self):
        return "SellPoint '" + self.name + "'"


class DropOff(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)

class CustomUser(AbstractUser):
    role = models.IntegerField(default=1)
    sellPoint = models.ForeignKey(SellPoint, null=True, default=None,
                                  on_delete=models.CASCADE, verbose_name="selling point (shop assistant)")
    balance = models.DecimalField(decimal_places=2, max_digits=30, default=Decimal(0))

    def is_user(self):
        return self.role == 1

    def is_store(self):
        assert (self.sellPoint is not None)
        return self.role == 2

    def is_admin(self):
        return self.role == 999



class Cup(models.Model):
    # Unique id
    id = models.IntegerField(primary_key=True, default=uuid.uuid4)
    size = models.IntegerField(default=0)
    timeIn = models.DateTimeField(null=True, default=None)
    timeEnd = models.DateTimeField(null=True, default=None)

    # Foreign Keys (can be null)
    # SellPoint shouldn't be empty while initializing!!!!!
    sellPoint = models.ForeignKey(SellPoint, on_delete=models.CASCADE, null=True)
    dropOff = models.ForeignKey(DropOff, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def assign_to_user(self, user: CustomUser):
        self.user = user

        assert (self.sellPoint is not None)
        assert (self.user is not None)
        assert (self.dropOff is None)

    def return_to_dropoff(self, dropOff: DropOff):
        self.dropOff = dropOff
        self.sellPoint = None

        assert (self.sellPoint is None)
        assert (self.user is not None)
        assert (self.dropOff is not None)

    def clean_at_dropoff(self):
        self.user = None

        assert (self.sellPoint is None)
        assert (self.user is None)
        assert (self.dropOff is not None)
