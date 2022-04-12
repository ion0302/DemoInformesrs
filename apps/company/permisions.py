from rest_framework.permissions import BasePermission

# from apps.users.models import UserMeta
#
#
# class UserHasPlan(BasePermission):
#     message = 'You are not buy any plan'
#
#     def has_permission(self, request, view):
#         user = request.user
#         if user.is_authenticated:
#             if UserMeta.objects.filter(user=user).count() == 0:
#                 return False
#
#             elif user.meta.plan is None:
#                 return False
#             else:
#                 return True
