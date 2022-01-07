from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def _create(self, phone, password, name, **extra_fields):
        if not phone:
            raise ValueError('Телефон не может быть пустым')
        user = self.model(phone=phone,
                          name=name,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, phone, password, name, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        return self._create(phone, password, name, **extra_fields)

    def create_superuser(self, phone, password, name, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self._create(phone, password, name, **extra_fields)


class User(AbstractBaseUser):
    phone = models.CharField(max_length=20,
                             primary_key=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=6,
                                       blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()

    def __str__(self):
        return self.phone

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff

    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(6, '0123456789')
        if User.objects.filter(activation_code=code).exists():
            self.create_activation_code()
        self.activation_code = code
        self.save()

    def send_activation_sms(self):
        from django.conf import settings
        from twilio.rest import Client

        message = f'Ваш код подтверждения: {self.activation_code}'

        client = Client(settings.TWILIO_SID,
                        settings.TWILIO_AUTH_TOKEN)

        client.messages.create(body=message,
                               from_=settings.TWILIO_NUMBER,
                               to=self.phone)
