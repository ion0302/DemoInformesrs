
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.company.models import Plan, Rule, Company
from apps.company.permisions import UserHasPlan
from apps.company.serializers import PlanSerializer, RuleSerializer, CompanySerializer

from rest_framework.throttling import UserRateThrottle


class PlanViewSet(ModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
    permission_classes = [IsAuthenticated]


class RuleViewSet(ModelViewSet):
    serializer_class = RuleSerializer
    queryset = Rule.objects.all()
    permission_classes = [IsAuthenticated]


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated, UserHasPlan]


