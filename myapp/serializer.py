from rest_framework import serializers


class TreeResourceSerializer(serializers.Serializer):
    excel = serializers.FileField()
