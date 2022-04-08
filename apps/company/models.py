from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Company(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=100, null=True)
    phone = PhoneNumberField(null=True)
    owner = models.CharField(max_length=100)

