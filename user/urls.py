from django.urls import path

from . import views

# /user/

app_name = "user"

urlpatterns = [
    path(
        "confirm-email/<uidb64>/<token>",
        views.ConfirmRegisterView.as_view(),
        name="activate",
    ),
    path(
        "reset-password",
        views.ResetPasswordView.as_view(),
        name="reset-password",
    ),
    path(
        "confirm-reset-password/<uidb64>/<token>",
        views.ConfirmResetPasswordView.as_view(),
        name="reset-password-confirm",
    ),
]
