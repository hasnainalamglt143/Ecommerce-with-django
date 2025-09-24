from django.db.models.signals import post_save

from django.contrib.auth.models import User

from store.models import Profile


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    print("Profile created for user:", instance.username)


post_save.connect(create_user_profile, sender=User)