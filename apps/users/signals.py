from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import UserMeta


@receiver(post_save, sender=UserMeta)
def set_rules(sender, instance, created, **kwargs):
    if created:
        if instance.plan:
            pass