from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(
        to=get_user_model(),
        related_name='profile',
        on_delete=models.CASCADE,
        verbose_name='Profile',
    )
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to='user_pics',
        verbose_name='Avatar',
    )
    github_link = models.URLField(
        null=True,
        blank=True,
        verbose_name='GitHub',
    )
    about_info = models.TextField(
        max_length=2000,
        null=True,
        blank=True,
        verbose_name='About info',
    )

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        