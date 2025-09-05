from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import ConfirmationCode, CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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

        try:
            confirmation_code = ConfirmationCode.objects.get(user=user)
        except ConfirmationCode.DoesNotExist:
            raise ValidationError('Код подтверждения не найден!')

        if confirmation_code.code != code:
            raise ValidationError('Неверный код подтверждения!')

        attrs['user'] = user
        return attrs

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['birthdate'] = str(user.birthdate) if user.birthdate else None
        return token