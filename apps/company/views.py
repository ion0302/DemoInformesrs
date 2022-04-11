
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.company.models import Plan, Rule
from apps.company.serializers import PlanSerializer, RuleSerializer


class PlanViewSet(ModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
    permission_classes = [IsAuthenticated]


class RuleViewSet(ModelViewSet):
    serializer_class = RuleSerializer
    queryset = Rule.objects.all()
    permission_classes = [IsAuthenticated]




