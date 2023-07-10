from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from checker.models import File, CheckStatus


class PyFileField(serializers.FileField):
    def to_internal_value(self, data):
        super().to_internal_value(data)
        if not data.name.endswith(".py"):
            raise ValidationError("File is not python file")
        return data


class FilesListCreateSerializer(serializers.ModelSerializer):
    filename = serializers.CharField(source="file.name", read_only=True)
    file = PyFileField(write_only=True)
    last_check_time = serializers.DateTimeField(source="last_check.datetime", read_only=True)
    last_check_status = serializers.CharField(source="last_check.status", read_only=True)

    class Meta:
        model = File
        fields = ["id", "filename", "last_check_time", "last_check_status", "file"]
        read_only_fields = ["id", "last_check_time", "last_check_status"]


class CheckStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckStatus
        fields = ["status", "datetime", "result"]


class OneFileSerializer(FilesListCreateSerializer):
    checks = serializers.ListSerializer(child=CheckStatusSerializer(), read_only=True)

    class Meta:
        model = File
        fields = [
            "id",
            "filename",
            "last_check_time",
            "last_check_status",
            "checks",
            "file",
        ]
        read_only_fields = ["id", "last_check_time", "last_check_status", "checks"]
