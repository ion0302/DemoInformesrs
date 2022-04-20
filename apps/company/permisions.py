from django.utils import timezone
from rest_framework.permissions import BasePermission

from apps.company.models import PlanLog, Rule, RequestLog


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
        aux_total = False
        aux_day = False
        pattern = view.get_model()
        action = view.get_action()
        resource = f'{pattern}.{action}'

        last_log = PlanLog.objects.filter(user=request.user).order_by('-pk').first()

        if last_log:
            instance = Rule.objects.filter(plan=last_log.plan, resource=resource).first()

            if instance:
                if not (instance.per_total and instance.per_day):
                    return True

                current_log = RequestLog.objects.filter(user=request.user,
                                                        pattern=pattern,
                                                        action=action,
                                                        plan_log=last_log).first()

                if not current_log:
                    return True

                elif current_log:
                    total_requests = current_log.count_total

                    if instance.per_total and total_requests < instance.per_total:
                        aux_total = True

                    day_requests = current_log.count_day

                    if instance.per_day and day_requests < instance.per_day or \
                            current_log.access_date.date() != timezone.now().date():
                        aux_day = True

                    if aux_day and aux_total:
                        return True

        return False
