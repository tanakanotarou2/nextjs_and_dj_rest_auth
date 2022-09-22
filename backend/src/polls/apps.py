from django.apps import AppConfig


class PollsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "polls"

    def ready(self):
        from project import container

        container.wire(modules=[".views"], packages=[".use_cases"])
