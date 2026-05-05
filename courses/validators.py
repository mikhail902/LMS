from rest_framework import serializers


def validate_youtube_link(value):
    if value and 'youtube.com' not in value:
        raise serializers.ValidationError('Разрешены ссылки только на youtube.com.')