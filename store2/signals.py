from django.db.models.signals import post_save
from django.dispatch import receiver
from Auth.models import User
from store.models import Shop
from django.contrib.auth import get_user_model


User = get_user_model()


@receiver(post_save, sender=User)
def create_shop(sender, instance, created, **kwargs):
    if created and instance.is_vendor:
        Shop.objects.create(
            user=instance, name=f"{instance.username} temporal", owner_email=instance.email
        )
