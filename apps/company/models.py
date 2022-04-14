from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models, router


class Plan(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = MoneyField(default_currency='USD', max_digits=10, decimal_places=2, null=True)


class Rule(models.Model):
    resource = models.CharField(max_length=200)
    per_day = models.PositiveIntegerField(null=True, default=None)
    per_total = models.PositiveIntegerField(null=True, default=None)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='plan_rules_set')


class PlanLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_planlog_set')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, related_name='plan_planlog_set')
    date_created = models.DateTimeField(default=timezone.now, blank=True, null=True)
    active_period = models.DurationField(blank=True, default=timedelta(seconds=0))

    def is_active(self):
        if self and self.date_created + self.active_period > timezone.now():
            return True
        else:
            return False


class Company(models.Model):
    name = models.CharField(max_length=200)
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=200)
