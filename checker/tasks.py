import pathlib

from celery import shared_task

from .models import File, CheckStatus
from .analyzer import analyze_file


@shared_task()
def check_by_flake8(file_id: int):
    try:
        file = File.objects.get(id=file_id)
    except File.DoesNotExist:
        return

    file_path = pathlib.Path(file.file.path)

    check_status = CheckStatus(file=file)

    try:
        result = analyze_file(file_path)
    except BaseException as error:
        print(error)
        check_status.status = CheckStatus.Status.FAIL
        check_status.result = str(error)
    else:
        if result:
            check_status.status = CheckStatus.Status.ERRORS
        else:
            check_status.status = CheckStatus.Status.SUCCESS
        check_status.result = result
    finally:
        check_status.save()
