from celery import shared_task
from celery.exceptions import Ignore
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

from .models import File, CheckStatus
from .analyzer import Analyzer


@shared_task()
def check_by_flake8(file_id: int) -> int:
    try:
        analyzer = Analyzer(file_id=file_id)
        result = analyzer.create_result()
        return result.id

    except File.DoesNotExist:
        raise Ignore()


@shared_task(ignore_result=True)
def send_result_by_email(check_id: int, user_id: int):
    try:
        check_status = CheckStatus.objects.select_related("file").get(id=check_id)
    except CheckStatus.DoesNotExist:
        return

    user_model = get_user_model()

    try:
        user = user_model.objects.get(id=user_id)
    except user_model.DoesNotExist:
        return

    email = EmailMultiAlternatives(
        subject=f"Результат анализа файла {check_status.file.file.name}",
        to=[user.email],
    )
    email.attach_alternative(check_status.result.replace("\n", "<br>"), "text/html")
    email.send()


@shared_task(ignore_result=True)
def send_user_statistic(user_id: int, files_count: int, checks_count: int):
    user_model = get_user_model()
    try:
        user = user_model.objects.get(id=user_id)
    except user_model.DoesNotExist:
        return

    email = EmailMultiAlternatives(
        subject=f"Статистика пользователя {user.username}",
        to=[user.email],
    )
    email.attach_alternative(
        f"У вас имеется {files_count} файлов.<br>"
        f"Всего проверок было совершено: {checks_count}.",
        "text/html",
    )
    email.send()


@shared_task(ignore_result=True)
def collect_statistic():
    for user in get_user_model().objects.all():
        files_count = user.file_set.count()
        checks_count = CheckStatus.objects.filter(file__user=user).count()
        send_user_statistic.delay(user.id, files_count, checks_count)
