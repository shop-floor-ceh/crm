from django.db import models
from account.models import Account


# Create your models here.
class Participant(models.Model):
    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    participant = models.ForeignKey(verbose_name='Участник', to=Account, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Имя роли', max_length=120)

    def __str__(self):
        return self.name


class Project(models.Model):
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    name = models.CharField(verbose_name='Имя проекта', max_length=120)
    synopsis = models.FileField(
        verbose_name='Синопис',
        upload_to=f'main/static/projects/{name}',
        blank=True
    )
    literary_script = models.FileField(
        verbose_name='Литературный сценарий',
        upload_to=f'main/static/projects/{name}',
        blank=True
    )
    directors_script = models.FileField(
        verbose_name='Режиссерский сценарий',
        upload_to=f'main/static/projects/{name}',
        blank=True
    )
    kpp = models.FileField(
        verbose_name='Календарно-постановочный план',
        upload_to=f'main/static/projects/{name}',
        blank=True
    )
    open_to_join = models.BooleanField(verbose_name='Открыт для входа', default=True)
    ended = models.BooleanField(verbose_name='Завершен', default=False)
    admin = models.ForeignKey(verbose_name='Админ', to=Account, on_delete=models.CASCADE)
    participants = models.ManyToManyField(
        verbose_name='Команда',
        to=Participant,
        blank=True
    )

    def __str__(self):
        return self.name


class Date(models.Model):
    class Meta:
        verbose_name = 'Дата встречи'
        verbose_name_plural = 'Даты встреч'

    project = models.ForeignKey(verbose_name='Проект', to=Project, on_delete=models.CASCADE)
    visiting_date = models.DateTimeField(verbose_name='Дата и время встречи')
    address = models.CharField(verbose_name='Адресс', max_length=250)
    setting = models.CharField(verbose_name='Сеттинг', max_length=250)
    scene = models.TextField(verbose_name='Сцены')

    def __str__(self):
        return f'{self.project}, {str(self.visiting_date).split()[0]}'
