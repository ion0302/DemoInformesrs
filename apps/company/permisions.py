from typing import List

from django.contrib.auth.models import User
from rest_access_policy import AccessPolicy
from rest_framework.permissions import BasePermission
from rest_framework.throttling import BaseThrottle

from apps.company.models import PlanLog, Company, Rule, Plan


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
    pass

#     """
#         Another way
#         """
#     # def get_policy_statements(self, request, view) -> List[dict]:
#     #     self.statements = []
#     #     queryset = Plan.objects.all()
#     #     last_log = PlanLog.objects.filter(user=request.user).last()
#     #     for i in queryset:
#     #         if last_log and last_log.plan == i:
#     #             rules = Rule.objects.filter(plan=i)
#     #             if rules:
#     #                 for j in rules:
#     #                     res = j.resource.split('.')
#     #                     pattern, action = res[0], res[1]
#     #                     if view.queryset.model.__name__ == pattern:
#     #                         self.statements += [{
#     #                             "action": [f'{action}'],
#     #                             "principal": "authenticated",
#     #                             "effect": "allow"
#     #                         }]
#     #     return self.statements
#
#     def has_permission(self, request, view) -> bool:
#         action = self._get_invoked_action(view)
#         endpoint_list = []
#         statements = []
#         last_log = PlanLog.objects.filter(user=request.user).last()
#         if last_log:
#             endpoint_list = list(Rule.objects.filter(plan=last_log.plan).values_list('resource', flat=True))
#         if f'{view.queryset.model.__name__}.{action}' in endpoint_list:
#             statements = [
#                 {
#                     "action": [f'{action}'],
#                     "principal": "*",
#                     "effect": "allow"
#                 }
#             ]
#
#         if len(statements) == 0:
#             return False
#
#         return self._evaluate_statements(statements, request, view, action)
#


class MainPermissions(BasePermission):

    def has_permission(self, request, view) -> bool:
        action = view.action
        endpoint_list = []
        last_log = PlanLog.objects.filter(user=request.user).last()
        if last_log:
            endpoint_list = list(Rule.objects.filter(plan=last_log.plan).values_list('resource', flat=True))
        if f'{view.queryset.model.__name__}.{action}' in endpoint_list:
            return True

        return False


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
