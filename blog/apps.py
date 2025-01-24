from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"

    def ready(self):
        @receiver(post_migrate)
        def create_default_groups(sender, **kwargs):
            from django.contrib.auth.models import Group
            Group.objects.get_or_create(name='Admin')
            Group.objects.get_or_create(name='User')