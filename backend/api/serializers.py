from rest_framework import serializers

from api.models import User
from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token
from utils import messages


class UserRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=True,
        min_length=2,
        max_length=128,
    )
    last_name = serializers.CharField(
        required=False,
        min_length=2,
        max_length=128,
    )
    phone = serializers.CharField(
        required=False,
        min_length=2,
        max_length=255,
        validators=[RegexValidator(
            regex=r'^\+?77(\d{9})$',
        )],
    )
    email = serializers.EmailField(
        required=True,
        min_length=3,
        max_length=255,
    )
    password = serializers.CharField(
        required=False,
        min_length=8,
        max_length=64,
        write_only=True,
    )
    token = serializers.CharField(
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'phone',
            'email',
            'password',
            'token',
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.get_or_create(user=user)
        token, _ = Token.objects.get_or_create(user=user)
        user.token = token.key
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        min_length=3,
        max_length=255,
        write_only=True,
    )
    password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=64,
        write_only=True,
    )
    token = serializers.CharField(
        required=False,
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'token',
        )

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = User.objects.filter(
            email=email
        ).first()
        if user is None:
            raise serializers.ValidationError(
                messages.USER_NOT_FOUND
            )
        if not user.is_active:
            raise serializers.ValidationError(
                messages.USER_NOT_ACTIVE
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                messages.INVALID_PASSWORD
            )
        token, _ = Token.objects.get_or_create(user=user)
        data['token'] = token.key
        return data


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
        )
