# dwitter/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Model to represent user profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followers",
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        """
        Signal receiver to create profile for new users and automatically follow themselves.
        """
        if created:
            # Create profile for new user
            Profile.objects.create(user=instance)
            # Make user follow themselves
            instance.profile.follows.add(instance.profile)