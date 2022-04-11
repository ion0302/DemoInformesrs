from django.contrib.auth.models import AbstractUser, User
from django.db import models

from apps.company.models import Plan


class UserManager(models.Model):
    user = models.OneToOneField(User, related_name='user_plan', on_delete=models.CASCADE, null=True)
    plan = models.ForeignKey(Plan, null=True, blank=True, on_delete=models.SET_NULL, related_name='plan_users_plans',
                             default=None)

