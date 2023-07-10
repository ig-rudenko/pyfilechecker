from celery import chain
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from checker.models import File
from checker.tasks import check_by_flake8, send_result_by_email
from .permissions import IsFileOwner
from .serializers import FilesListCreateSerializer, OneFileSerializer


class FilesListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = FilesListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        file_obj: File = serializer.save(user=self.request.user)
        chain_tasks = chain(
            check_by_flake8.s(file_obj.id), send_result_by_email.s(self.request.user.id)
        )

        chain_tasks()


class OneFileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsFileOwner]
    serializer_class = OneFileSerializer
    queryset = File.objects.all()

    def post(self, request, *args, **kwargs):
        file = self.get_object()

        chain_tasks = chain(
            check_by_flake8.s(file.id), send_result_by_email.s(self.request.user.id)
        )
        chain_tasks()
        return Response({"result": "ok", "message": "file under testing"})

    def perform_update(self, serializer):
        old_file: File = self.get_object()
        old_file.file.delete()
        serializer.save()
