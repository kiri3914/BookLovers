from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Activity, Review


@receiver(post_save, sender=Review)
def create_activity(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(review=instance)

