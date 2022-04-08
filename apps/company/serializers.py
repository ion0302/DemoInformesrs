from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.company.models import Company


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
