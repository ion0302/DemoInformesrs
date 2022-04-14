from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.company.models import Plan, Rule, Company, PlanLog, RequestLog


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


class PlanLogSerializer(ModelSerializer):
    class Meta:
        model = PlanLog
        fields = '__all__'


class RequestLogSerializer(ModelSerializer):
    class Meta:
        model = RequestLog
        fields = '__all__'
