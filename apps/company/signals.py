from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.company.models import PlanLog, Rule


# Block save if user has an active plan
@receiver(pre_save, sender=PlanLog)
def block_save(sender, instance, **kwargs):
    last_log = PlanLog.objects.filter(user=instance.user).last()
    if last_log and last_log.plan and last_log.is_active():
        raise Exception("User already has a plan")


@receiver(post_save, sender=PlanLog)
def set_rules(sender, instance, created, **kwargs):
    if created:
        plan_object = instance.plan
        rules_queryset = Rule.objects.filter(plan=plan_object)
        for i in rules_queryset:
            res = i.resource.split('.')
            pattern, action = res[0], res[1]

            """
            #for instance.user set
            -rule1
            -rule2
            """


@receiver(post_save, sender=Rule)
def update_plan(sender, instance, created, **kwargs):
    if created:
        """
        repeat loop for set permisions
        """
        pass
