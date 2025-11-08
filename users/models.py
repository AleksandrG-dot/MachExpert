from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser):
    patronymic = models.CharField(max_length=150, blank=True, verbose_name="Отчество")
    service_number = models.CharField(
        max_length=5, unique=True, verbose_name="Табельный номер"
    )
    internal_phone = models.CharField(
        max_length=5, blank=True, null=True, verbose_name="Вн. номер"
    )
    mobile_phone = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Моб. номер"
    )
    position = models.CharField(
        max_length=150, blank=False, null=False, verbose_name="Должность"
    )
    birthday = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    date_employment = models.DateField(
        blank=True, null=True, verbose_name="Дата приема"
    )
    date_dismissal = models.DateField(
        blank=True, null=True, verbose_name="Дата увольнения"
    )
    comment = models.TextField(
        blank=True, help_text="Введите примечание", verbose_name="Примечание"
    )

    REQUIRED_FIELDS = ["position", "service_number"]

    def __str__(self):
        return f"{self.username}".strip()

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
