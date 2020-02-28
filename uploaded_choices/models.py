from company.models import Company
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
from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize= value.size
    
    if filesize > 429916160:
        raise ValidationError("The maximum file size that can be uploaded is 500MB")
    else:
        return value

def user_directory_path(instance, name):
    return 'company_{0}/user_{1}/{2}'.format(instance.company.id, instance.user.id, name)


class UploadedFile(models.Model):
    class UploadedFileChoices(Enum):
        video = 'v'
        media_record = 'm'
        audio_record = 'a'
        image = 'i'
        preview = 'p'
        issue = 's'
    symbol = models.CharField(null=False, max_length=1)
    file = models.FileField(upload_to=user_directory_path, validators=[validate_file_size])
    user = models.ForeignKey(User, models.CASCADE, null=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True)
    type = models.CharField(null=False, max_length=1)

    @property
    def type_enum(self):
        return self.UploadedFileChoices(self.type)

    @type_enum.setter
    def type_enum(self, p_type):
        self.type = p_type.value

    def __str__(self):
        return f"{self.user} - {self.company.name}"
