from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    """When creating a new User also create a new Profile"""
    if kwargs.get('created', False):
        Profile(user=kwargs.get('instance')).save()
