from rest_framework import serializers
from .models import URL


class URLSerializer(serializers.ModelSerializer):
    """
    Serializer for the URL model.
    Handles validation of incoming URL data
    and serialization of outgoing responses.
    """

    class Meta:
        model = URL
        fields = ['id', 'original_url', 'short_code', 'created_at', 'click_count']
        read_only_fields = ['id', 'short_code', 'created_at', 'click_count']


class URLCreateSerializer(serializers.ModelSerializer):
    """
    Serializer specifically for creating a new short URL.
    Only accepts original_url as input from the user.
    Everything else is generated or set automatically.
    """

    class Meta:
        model = URL
        fields = ['original_url']

    def validate_original_url(self, value):
        """
        Custom validation for the original_url field.
        Runs automatically when .is_valid() is called.
        """

        # Strip whitespace from both ends
        value = value.strip()

        # Must start with http:// or https://
        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError(
                "URL must start with http:// or https://"
            )

        # Reject unreasonably short URLs (e.g. "http://x")
        if len(value) < 11:
            raise serializers.ValidationError(
                "Please enter a valid, complete URL."
            )

        return value