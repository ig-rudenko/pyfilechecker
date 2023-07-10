from functools import cached_property

from django.db import models


def upload_to(instance: "File", file_name: str) -> str:
    return f"{instance.user.username}/{file_name}"


class File(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    mod_time = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to=upload_to)

    class Meta:
        db_table = "files"

    def __str__(self):
        return f"File: {self.file.name}"

    @cached_property
    def last_check(self) -> "CheckStatus":
        return self.checks.first()


class CheckStatus(models.Model):
    class Status(models.TextChoices):
        NON_CHECKED = "NCK", "Не проверенный"
        SUCCESS = "SCS", "Нет ошибок"
        ERRORS = "ERR", "Есть ошибки"
        FAIL = "FAL", "Ошибка анализа"

    status = models.CharField(
        choices=Status.choices, max_length=3, default=Status.NON_CHECKED
    )
    datetime = models.DateTimeField(auto_now_add=True)
    result = models.TextField(default="")
    file = models.ForeignKey("File", on_delete=models.CASCADE, related_name="checks")

    class Meta:
        db_table = "checks"
        ordering = ["-datetime"]
