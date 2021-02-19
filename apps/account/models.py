from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


class UserManagerToUser(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_phone, password, **extra_fields):
        """ Создает и сохраняет пользователя с введенным им email и паролем """
        if not user_phone:
            raise ValueError('телефон должен быть указан')

        user = self.model(user_phone=user_phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_phone, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_phone, password, **extra_fields)

    def create_superuser(self, user_phone, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(user_phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Компания', 'Компания'), ('Судья', 'Судья'),
        ('Судебный пристав', 'Судебный пристав'), ('Администратор', 'Администратор'),
    )
    email = models.EmailField(verbose_name='Email', blank=True)
    first_name = models.CharField(verbose_name='name', max_length=30, blank=True)
    last_name = models.CharField(verbose_name='surname', max_length=30, blank=True)
    user_phone = models.BigIntegerField(verbose_name='Номер телефона', blank=True, null=True, unique=True)
    user_role = models.CharField(verbose_name='Роль Пользователя', max_length=30, choices=ROLE_CHOICES, blank=True)
    user_inn = models.CharField(max_length=12, verbose_name='ИНН Пользователя', blank=True)
    is_active = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(verbose_name='registered', auto_now_add=True)

    objects = UserManagerToUser()

    USERNAME_FIELD = 'user_phone'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def get_full_name(self):
        """ Возвращает first_name и last_name с пробелом между ними """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """ Возвращает сокращенное имя пользователя"""
        return self.first_name


class Company(models.Model):
    """ Модель компании"""
    user_profile = models.ForeignKey(User, related_name='companies', on_delete=models.CASCADE,
                                     verbose_name='Компания Пользователя')
    name_full = models.CharField(max_length=100, verbose_name='Наименование компании (полное)')
    name_short = models.CharField(max_length=100, verbose_name='Наименование компании (сокр)', blank=True)
    okopf = models.CharField(max_length=100, verbose_name='ОКОПФ или вид компании', blank=True)
    inn = models.CharField(max_length=100, verbose_name='ИНН компании', blank=True)
    kpp = models.CharField(max_length=100, verbose_name='КПП компании', blank=True)
    ogrn = models.CharField(max_length=100, verbose_name='ОГРН компании', blank=True)
    type = models.CharField(max_length=100, verbose_name='Тип компании', blank=True)
    ogrn_data_reg = models.CharField(max_length=100, verbose_name='Дата выдачи ОГРН компании', blank=True)
    director = models.CharField(max_length=100, verbose_name='Директор компании', blank=True)
    adress = models.CharField(max_length=200, verbose_name='Адрес компании', blank=True)

    objects = UserManager()

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return self.name_full


