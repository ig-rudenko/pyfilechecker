from django.urls import path

from . import views

# /api/

urlpatterns = [
    path("files", views.FilesListCreateAPIView.as_view()),
    path("files/<int:pk>", views.OneFileAPIView.as_view()),
]
