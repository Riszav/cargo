from celery import shared_task
from django.core.mail import send_mail


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_task(
    self,
    subject,
    message,
    from_email,
    recipient_list,
    html_message=None,
    fail_silently=False,
):
    try:
        return send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=fail_silently,
        )
    except Exception as exc:
        raise self.retry(exc=exc)
