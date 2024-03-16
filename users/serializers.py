from rest_framework import serializers
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data returning in the post data"""

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for handling users registering"""

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

    def validate_email(self, value):
        """
        Check if the email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email address already exists try login.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for handling auth token
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """
        Validate and authenticate the user
        """
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=email.lower(),
            password=password,
        )
        if not user:
            msg = _("Unable to authenticate with these credintials")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
