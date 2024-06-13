from rest_framework import serializers

from .models import ClaimReport


class ClaimReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimReport
        fields = "__all__"
