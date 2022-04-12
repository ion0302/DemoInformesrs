from django.contrib.auth.models import User
from django.utils import timezone
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models


class Plan(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = MoneyField(default_currency='USD', max_digits=10, decimal_places=2, null=True)
    date_created = models.DateField(default=timezone.now, blank=True)
    date_active = models.DateField(default=timezone.now, blank=True)


class Rule(models.Model):
    resource = models.CharField(max_length=200)
    per_day = models.PositiveIntegerField(null=True, default=None)
    per_total = models.PositiveIntegerField(null=True, default=None)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='plan_rules_set')


class Company(models.Model):
    name = models.CharField(max_length=200)
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=200)
