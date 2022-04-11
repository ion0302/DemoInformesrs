from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.company.models import Plan, Rule, Company


class PlanSerializer(ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class RuleSerializer(ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
