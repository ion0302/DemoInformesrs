from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField

from django.db import models


class Plan(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = MoneyField(default_currency='USD', max_digits=10, decimal_places=2, null=True)


class Rule(models.Model):
    class Meta:
        unique_together = [
            ('plan', 'resource')
        ]

    resource = models.CharField(max_length=200)
    per_total = models.PositiveIntegerField(null=True, default=None, blank=True)
    per_day = models.PositiveIntegerField(null=True, default=None, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='plan_rules_set')

    def clean(self):
        if self.per_total and self.per_day:
            if self.per_total < self.per_day:
                raise ValidationError("Number of requests per_day can't be biggest than per_total")
            elif self.per_day == 0 or self.per_total == 0:
                raise ValidationError("You cannot assign a value equal to 0")


class PlanLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_planlog_set')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, related_name='plan_planlog_set')
    date_created = models.DateTimeField(default=timezone.now, blank=True, null=True)
    active_period = models.DurationField(blank=True, default=timedelta(seconds=0))

    def is_active(self):
        if self and self.date_created < timezone.now() < self.date_created + self.active_period:
            return True
        else:
            return False

    def clean(self):
        last_log = PlanLog.objects.filter(user=self.user).order_by('-pk').first()
        if self != last_log and last_log and last_log.plan and last_log.is_active():
            raise ValidationError("User already has a plan")


class RequestLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_requestlog_set')
    pattern = models.CharField(max_length=50)
    action = models.CharField(max_length=50)
    access_date = models.DateTimeField(blank=True, default=timezone.now)
    plan_log = models.ForeignKey(PlanLog, on_delete=models.CASCADE, related_name='plan_log_requestlog_set')
    count_total = models.PositiveIntegerField(default=0)
    count_day = models.PositiveIntegerField(default=0)

    def count(self):
        self.count_day += 1
        self.count_total += 1


class Company(models.Model):
    name = models.CharField(max_length=200)
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=200)
