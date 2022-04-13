from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.company.models import Plan, Rule, Company, PlanLog
from apps.company.permisions import UserHasActivePlan, SimpleAccessPolicy, VIPAccessPolicy

from apps.company.serializers import PlanSerializer, RuleSerializer, CompanySerializer, PlanLogSerializer


class PlanViewSet(ModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
    permission_classes = [IsAuthenticated]


class RuleViewSet(ModelViewSet):
    serializer_class = RuleSerializer
    queryset = Rule.objects.all()
    permission_classes = [IsAuthenticated]


class PlanLogViewSet(ModelViewSet):
    serializer_class = PlanLogSerializer
    queryset = PlanLog.objects.all()
    permission_classes = [IsAuthenticated]


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated, UserHasActivePlan]
  #  permission_classes = (SimpleAccessPolicy,)




    def get_permissions(self):
        # instance = PlanLog.objects.filter(user=self.request.user).filter(plan__name='Simple').last()
        # if instance and instance.is_active():
        #     self.permission_classes = [SimpleAccessPolicy]
        instance = PlanLog.objects.filter(user=self.request.user).last()
        if instance and instance.plan.name == 'Simple':
            self.permission_classes = [SimpleAccessPolicy]
        if instance and instance.plan.name == 'VIP':
            self.permission_classes = [VIPAccessPolicy]

        return super(CompanyViewSet, self).get_permissions()



