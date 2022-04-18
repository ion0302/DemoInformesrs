from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.company.models import Company, PlanLog
from apps.company.permisions import UserHasActivePlan, MainPermissions

from apps.company.serializers import CompanySerializer, PlanLogSerializer


class PlanLogViewSet(ModelViewSet):
    serializer_class = PlanLogSerializer
    queryset = PlanLog.objects.all()
    permission_classes = [IsAuthenticated, MainPermissions]


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated, UserHasActivePlan, MainPermissions]

    @action(detail=False, methods=['GET'])
    def test_action(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

