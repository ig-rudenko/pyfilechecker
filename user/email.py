from django.http import HttpRequest
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string


class BaseEmailSender:
    template_name = ""
    user_field = "id"

    def __init__(self, current_site: str, user: AbstractUser):
        self.current_site = current_site
        self._user = user

    def get_template_name(self) -> str:
        if not self.template_name:
            raise NotImplemented("Не был указан шаблон для отправки email")
        return self.template_name

    def get_domain(self) -> str:
        return self.current_site

    def get_uid_base64(self) -> str:
        user_field_data = getattr(self._user, self.user_field)
        # Если `user_field == "id"`, то это равносильно `self._user.id`

        return urlsafe_base64_encode(force_bytes(user_field_data))

    def get_user_token(self) -> str:
        return default_token_generator.make_token(self._user)

    def get_context(self) -> dict:
        return {
            "user": self._user,
            "domain": self.get_domain(),
            "uid": self.get_uid_base64(),
            "token": self.get_user_token(),
        }

    def get_message(self) -> str:
        return render_to_string(self.get_template_name(), self.get_context())

    def get_subject(self) -> str:
        return f"Подтвердите регистрацию на сайте {self.get_domain()}"

    def perform_send_email(self):
        message = self.get_message()
        email = EmailMultiAlternatives(
            subject=self.get_subject(),
            body=message,
            to=[self._user.email],
        )
        email.attach_alternative(message, "text/html")
        email.send()

    def send_email(self):
        return self.perform_send_email()


class RegisterConfirmEmailSender(BaseEmailSender):
    template_name = "registration/email_confirm.html"

    def get_context(self) -> dict:
        ctx = super().get_context()
        ctx["variable"] = "Привет"
        return ctx


class ResetPasswordEmailSender(BaseEmailSender):
    template_name = "registration/email_reset_password_confirm.html"
