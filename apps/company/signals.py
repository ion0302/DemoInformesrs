from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.company.models import PlanLog, Rule


@receiver(post_save, sender=PlanLog)
def set_rules(sender, instance, created, **kwargs):
    if created:
        plan_object = instance.plan
        rules_queryset = Rule.objects.filter(plan=plan_object)
        for i in rules_queryset:
            res = i.resource.split('.')
            pattern, action = res[0], res[1]



