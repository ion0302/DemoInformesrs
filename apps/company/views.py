from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import is_success
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from apps.company.models import Company, PlanLog, RequestLog
from apps.company.permisions import UserHasActivePlan, MainPermissions

from apps.company.serializers import CompanySerializer, PlanLogSerializer


class ResourceViewSet(GenericViewSet):
    model_name: str
    action_name: str

    def get_model(self) -> str:
        return getattr(self, 'model_name', f'{self.queryset.model.__name__}')

    def get_action(self) -> str:
        return getattr(self, 'action_name', f'{self.action}')

    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """

        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        pattern = self.get_model()
        action = self.get_action()

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)

        if is_success(self.response.status_code):
            last_log = PlanLog.objects.filter(user=request.user).order_by('-pk').first()
            instance, created = RequestLog.objects.get_or_create(user=request.user,
                                                                 pattern=pattern,
                                                                 action=action,
                                                                 plan_log=last_log)

            if instance.access_date.date() != timezone.now().date():
                instance.count_day = 0

            instance.access_date = timezone.now()
            instance.count()
            instance.save()

        return self.response


class PlanLogViewSet(ModelViewSet, ResourceViewSet):
    serializer_class = PlanLogSerializer
    queryset = PlanLog.objects.all()
    permission_classes = [IsAuthenticated, UserHasActivePlan, MainPermissions]


class CompanyViewSet(ModelViewSet, ResourceViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated, UserHasActivePlan, MainPermissions]

    resource_name = 'test.aaa'

    @action(detail=False, methods=['GET'])
    def test_action(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
