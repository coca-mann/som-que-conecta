from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, UserType


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        default_type, _ = UserType.objects.get_or_create(name='Padrão')
        UserProfile.objects.create(user=instance, user_type=default_type)
    else:
        instance.userprofile.save()
