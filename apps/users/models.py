from django.contrib.auth.models import AbstractUser, User
from django.db import models

from apps.company.models import Plan


class UserMeta(models.Model):
    user = models.OneToOneField(User, related_name='meta', on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, null=True, blank=True, on_delete=models.SET_NULL, related_name='user_plan',
                             default=None)



