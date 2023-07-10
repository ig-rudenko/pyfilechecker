from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site

from .forms import UserRegisterForm, ResetPasswordForm, EmailForm
from .email import RegisterConfirmEmailSender, ResetPasswordEmailSender
from .tasks import send_register_email


class Register(View):
    def get(self, request):
        return render(
            request, "registration/register.html", {"form": UserRegisterForm()}
        )

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if not form.is_valid():
            return render(request, "registration/register.html", {"form": form})

        user = form.save(commit=False)  # Создаем объект, без сохранения в БД
        user.is_active = False
        user.save()

        current_site = str(get_current_site(request))

        # Email Task
        send_register_email.delay(current_site, user.id)

        return redirect(reverse("accounts:login"))


class ConfirmRegisterView(View):
    def get(self, request, uidb64: str, token: str):
        uid = force_str(
            urlsafe_base64_decode(uidb64)
        )  # Получаем идентификатор пользователя
        user = get_object_or_404(get_user_model(), id=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("<h1>Спасибо, что подтвердили регистрацию!</h1>")

        return HttpResponse("<h1>Ссылка неверная</h1>")


class ResetPasswordView(View):
    def get(self, request):
        return render(
            request, "registration/reset_password.html", {"form": EmailForm()}
        )

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(get_user_model(), email=form.cleaned_data["email"])
            email_sender = ResetPasswordEmailSender(request, user)
            email_sender.send_email()
            return HttpResponse("<h1>Проверьте почту, для сброса пароля!</h1>")

        return render(request, "registration/reset_password.html", {"form": form})


class ConfirmResetPasswordView(View):
    def get(self, request, uidb64: str, token: str):
        return render(
            request,
            "registration/confirm_reset_password.html",
            {"form": ResetPasswordForm()},
        )

    def post(self, request, uidb64: str, token: str):
        # Пример URL /Mjg/bqgzrh-6147c5ab396a08a5541ceb05e6c11e01

        uid = force_str(
            urlsafe_base64_decode(uidb64)
        )  # Получаем идентификатор пользователя из `Mjg`
        user = get_object_or_404(get_user_model(), id=uid)

        form = ResetPasswordForm(request.POST)
        # Проверяем форму и токен - `bqgzrh-6147c5ab396a08a5541ceb05e6c11e01`
        if form.is_valid() and default_token_generator.check_token(user, token):
            user.set_password(form.cleaned_data["password1"])
            user.save()
            return redirect(reverse("accounts:login"))

        return render(request, "registration/reset_password.html", {"form": form})
