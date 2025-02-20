from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'email_notifications', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }


    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise ValidationError('Email is required')
        if not password:
            raise ValidationError('Password is required')

        user = authenticate(email=email, password=password)

        if not user:
            raise ValidationError('Invalid email or password')

        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        tokens = RefreshToken.for_user(user)

        return {
            'access_token': str(tokens.access_token),
            'refresh_token': str(tokens),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email_notifications': user.email_notifications
            }
        }
