from django.db import models
import datetime
from django.utils import timezone
from users.models import CustomUser
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
from enum import Enum
import random
import string
from django.utils import timezone
User = get_user_model()


class UploadedFile(models.Model):
    class UploadedFileChoices(Enum):
        video = 'v'
        media_record = 'm'
        audio_record = 'a'
        image = 'i'
        preview = 'p'
        issue = 's'
    symbol = models.CharField(null=False, max_length=1)
    file = models.FileField(upload_to='get_random_path', null=True)
    user = models.ForeignKey(User, models.CASCADE, null=False)
    type = models.CharField(null=False, max_length=1)

    @property
    def type_enum(self):
        return self.UploadedFileChoices(self.type)

    @type_enum.setter
    def type_enum(self, p_type):
        self.type = p_type.value