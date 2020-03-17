from django.db import models
from django.conf import settings
from datetime import datetime
from users.models import CustomUser
from django.utils.encoding import python_2_unicode_compatible
from company.models import Company
from django.utils.translation import ugettext_lazy as _


class News(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news_of_user')
    company = models.ForeignKey(Company, blank=True, null=True,
                              default=None, on_delete=models.CASCADE, related_name="news_of_company")
    status = models.BooleanField(default=True)
    is_active = models.BooleanField(_('active'), default=True)
    publish_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return '"%s" by %s' % (self.title, self.user)
