from rest_framework import serializers

from users.models import UsedViewsLogs


class LogSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UsedViewsLogs
        fields = "__all__"
