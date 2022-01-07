from django.contrib.auth import get_user_model
from rest_framework import serializers



User = get_user_model()

class RegistrationSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20,
                                  required=True)
    name = serializers.CharField(max_length=50,
                                 required=True)
    password = serializers.CharField(min_length=6,
                                     required=True)
    password_confirm = serializers.CharField(min_length=6,
                                             required=True)

    def validate_phone(self, phone):
        import re
        phone = re.sub('[^0-9]', '', phone)
        if phone.startswith('0'):
            phone = f'996{phone[1:]}'
        phone = f'+{phone}'
        if len(phone) != 13 and not phone.startswith('+996'):
            raise serializers.ValidationError('Неверный формат номера')
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError('Номер уже занят')
        return phone

    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.pop('password_confirm')
        if password1 != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self):
        user = User.objects.create_user(**self.validated_data)
        user.create_activation_code()
        user.send_activation_sms()


class ActivationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6,
                                 min_length=6,
                                 required=True)

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return code

    def activate(self):
        code = self.validated_data.get('code')
        user = User.objects.get(activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(min_length=6, required=True)

    def validate_phone(self, phone):
        import re
        phone = re.sub('[^0-9]', '', phone)
        if phone.startswith('0'):
            phone = f'996{phone[1:]}'
        phone = f'+{phone}'
        if len(phone) != 13 and not phone.startswith('+996'):
            raise serializers.ValidationError('Неверный формат номера')
        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return phone

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        user = User.objects.get(phone=phone)
        if not user.is_active:
            raise serializers.ValidationError('Пользователь не активен')
        if not user.check_password(password):
            raise serializers.ValidationError('Неверный пароль')
        attrs['user'] = user
        return attrs


class LogOutSerializer(serializers.Serializer):
    pass


class ChangePasswordSerializer(serializers.Serializer):
    pass


class ForgotPasswordSerializer(serializers.Serializer):
    pass
