from typing import List

from django.contrib.auth.models import User
from django.utils import timezone
from rest_access_policy import AccessPolicy
from rest_framework.permissions import BasePermission

from apps.company.models import PlanLog, Company, Rule, Plan, RequestLog


class UserHasActivePlan(BasePermission):
    message = 'You do not have access'

    def has_permission(self, request, view):
        user = request.user
        instance = PlanLog.objects.filter(user=user).order_by('-pk').first()

        if user.is_authenticated:
            if PlanLog.objects.filter(user=user).count() == 0:
                return False
            elif instance.is_active():
                return True
            else:
                return False


class MainPermissions(BasePermission):

    def has_permission(self, request, view) -> bool:
        action = view.action
        aux_total = False
        aux_day = False
        pattern = view.queryset.model.__name__
        resource = f'{view.queryset.model.__name__}.{action}'
        endpoint_list = []

        last_log = PlanLog.objects.filter(user=request.user).order_by('-pk').first()

        if last_log:
            instance = Rule.objects.get(plan=last_log.plan, resource=resource)

            if instance:
                if instance.per_day == 0 and instance.per_total == 0:
                    return False

                elif not (instance.per_total and instance.per_day):
                    return True

                total_requests = RequestLog.objects.filter(user=request.user,
                                                           pattern=pattern,
                                                           action=action,
                                                           plan_log=last_log).count()

                if instance.per_total and total_requests < instance.per_total:
                    aux_total = True

                day_requests = RequestLog.objects.filter(access_date__date=timezone.now().date(),
                                                         user=request.user,
                                                         pattern=pattern,
                                                         action=action,
                                                         plan_log=last_log).count()

                if instance.per_day and day_requests < instance.per_day:
                    aux_day = True

                if aux_day and aux_total:
                    RequestLog.objects.create(user=request.user,
                                              pattern=pattern,
                                              action=action,
                                              access_date=timezone.now(),
                                              plan_log=last_log)
                    return True

            return False

        return False
