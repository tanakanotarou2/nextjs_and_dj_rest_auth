
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()

    profile_icon = models.ImageField(_("profile icon"), upload_to="profile_icons", null=True, blank=True)
