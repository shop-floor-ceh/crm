from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, photo=None, phone=None, about_me=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            photo=photo,
            phone=phone,
            about_me=about_me,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password, photo=None, phone=None, about_me=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            photo=photo,
            phone=phone,
            about_me=about_me,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'

    email = models.EmailField(verbose_name='email', unique=True, max_length=120)
    username = models.CharField(verbose_name='username', max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(verbose_name='first name', max_length=30)
    last_name = models.CharField(verbose_name='last name', max_length=60)
    phone = models.CharField(verbose_name='phone', max_length=15, blank=True, default=0)
    photo = models.ImageField(verbose_name='photo', blank=True, default='', upload_to='account/static/profile')
    about_me = models.TextField(verbose_name='about me', blank=True, default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]

    objects = MyAccountManager()

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_active


class SocialNetworks(models.Model):
    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    link = models.URLField(verbose_name='link', )

    def __str__(self):
        return f'{self.link}'


class Notification(models.Model):
    class Meta:
        verbose_name = 'Уведомления'
        verbose_name_plural = 'Уведомления'

    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    mail = models.BooleanField(verbose_name='mail', default=False)
    telegram = models.BooleanField(verbose_name='telegram', default=False)
    vk = models.BooleanField(verbose_name='vk', default=False)

    def __str__(self):
        return f'{self.user}'
