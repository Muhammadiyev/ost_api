from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from news.models import New
from comment.models import Comment


@receiver(post_save, sender=Comment)
def send_notification(sender, instance, created, **kwargs):
    if created:
        comment_id = instance.id
        news = New.objects.get(news__id=comment_id)
        subscriber = news.subscribers.values_list('email')
        subscribers_emails = [x for (x,) in subscriber]
        print(subscribers_emails)
        for email in subscribers_emails:
            send_mail('People are commented', 'People are commented to news your subscribed for',
                      settings.EMAIL_HOST_USER,
                      recipient_list=[email])
