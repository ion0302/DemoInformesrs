from django.contrib.auth.models import User
from django.utils import timezone
from djmoney.models.fields import MoneyField
from django.db import models


class Plan(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = MoneyField(default_currency='USD', max_digits=10, decimal_places=2, null=True)
    date_created = models.DateField(default=timezone.now, blank=True)
    date_active = models.DateField(default=timezone.now, blank=True)


class Rule(models.Model):
    resource = models.CharField(max_length=200)
    plan = models.OneToOneField(Plan, null=True, on_delete=models.SET_NULL, related_name='plan')
    per_day = models.PositiveIntegerField(null=True, default=None)
    per_total = models.PositiveIntegerField(null=True, default=None)




