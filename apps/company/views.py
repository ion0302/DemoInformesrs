from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
    permission_classes = [IsAuthenticated, SimpleAccessPolicy]


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated, UserHasActivePlan, SimpleAccessPolicy]

    @action(detail=False, methods=['GET'])
    def test_action(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    # def get_permissions(self):
    #     instance = PlanLog.objects.filter(user=self.request.user).last()
    #     if instance and instance.plan.name == 'Simple':
    #         self.permission_classes = [SimpleAccessPolicy, UserHasActivePlan]
    #     if instance and instance.plan.name == 'VIP':
    #         self.permission_classes = [VIPAccessPolicy, UserHasActivePlan]
    #
    #     return super(CompanyViewSet, self).get_permissions()



