from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.cache import cache
from users.models import CustomUser


class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class AuthValidateSerializer(UserBaseSerializer):
    pass


class RegisterValidateSerializer(UserBaseSerializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Email уже существует!')
        return email

    def validate_phone_number(self, phone_number):
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('Телефон уже используется!')
        return phone_number


class ConfirmationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        code = attrs.get('code')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise ValidationError('User не существует!')

        redis_key = f"confirm_code:{user_id}"
        stored_code = cache.get(redis_key)

        if stored_code is None:
            raise ValidationError('Код подтверждения не найден или истёк!')

        if stored_code != code:
            raise ValidationError('Неверный код подтверждения!')

        cache.delete(redis_key)

        attrs['user'] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['birthdate'] = str(user.birthdate) if user.birthdate else None
        return token
