from celery import shared_task

from .email import RegisterConfirmEmailSender
from .models import User


@shared_task()
def send_register_email(domain: str, user_id: int) -> bool:
    print("start send_register_email")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return False

    # Email
    email_sender = RegisterConfirmEmailSender(
        domain,
        user,
    )
    email_sender.send_email()
    print("end send_register_email")

    return True
