from django.contrib.auth.models import User
from rest_access_policy import AccessPolicy
from rest_framework.permissions import BasePermission

from apps.company.models import PlanLog




class UserHasActivePlan(BasePermission):
    message = 'You are not buy any plan'

    def has_permission(self, request, view):
        user = request.user
        instance = PlanLog.objects.filter(user=user).last()

        if user.is_authenticated:
            if PlanLog.objects.filter(user=user).count() == 0:
                return False
            elif instance.is_active():
                return True
            else:
                return False


# class CompanyAccessPolicy(AccessPolicy):
#     statements = [
#         {
#             "action": ["list", "retrieve"],
#             "principal": "*",
#             "effect": "allow"
#         },
#         {
#             "action": ["publish", "unpublish"],
#             "principal": ["group:editor"],
#             "effect": "allow"
#         }
#     ]


