from django.contrib.auth.models import User
from rest_access_policy import AccessPolicy
from rest_framework.permissions import BasePermission

from apps.company.models import PlanLog, Company, Rule


class UserHasActivePlan(BasePermission):
    message = 'You are not authorized'

    def has_permission(self, request, view):
        user = request.user
        instance = PlanLog.objects.filter(user=user).last()

        # each endpoint request

        if user.is_authenticated:
            if PlanLog.objects.filter(user=user).count() == 0:
                return False
            elif instance.is_active():
                return True
            else:
                return False


class SimpleAccessPolicy(AccessPolicy):
    statements = []
    queryset = Rule.objects.filter(plan__name='Simple')
    if queryset:
        for i in queryset:
            res = i.resource.split('.')
            pattern, action = res[0], res[1]
            rule = {
                "action": [f'{action}'],
                "principal": "*",
                "effect": "allow"
            }
            statements.append(rule)


class VIPAccessPolicy(AccessPolicy):
    statements = []
    queryset = Rule.objects.filter(plan__name='VIP')
    if queryset:
        for i in queryset:
            res = i.resource.split('.')
            pattern, action = res[0], res[1]
            rule = {
                "action": [f'{action}'],
                "principal": "*",
                "effect": "allow"
            }
            statements.append(rule)

#no update after add new rules
#change update statement after add new rule
#change statement from list to unique values