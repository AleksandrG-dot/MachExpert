from django.db import models
from django.urls import reverse

from config.settings import ORDER_STATUS, PPS_CP_STATUS, PRODUCTION_STATUS
from users.models import Employee


class Order(models.Model):
    """Модель “Заказ”"""

    number_bn = models.CharField(max_length=5, unique=True, verbose_name="Номер СЗ")
    responsible = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Ответственный менеджер",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Сумма заказа",
    )

    folder_bn = models.URLField(
        blank=True,
        verbose_name="Ссылка на папку с СЗ",
        help_text=r"Формат: \\server\share\folder или file:///C:/Path/To/Folder/",
    )

    order_status = models.CharField(
        max_length=10,
        choices=ORDER_STATUS,
        default="created",
        verbose_name="Статус заказа",
    )
    date_created = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    folder_documentation = models.URLField(
        blank=True,
        verbose_name="Ссылка на папку с документацией",
        help_text=r"Формат: \\server\share\folder или file:///C:/Path/To/Folder/",
    )
    date_completion = models.DateField(
        blank=True, null=True, verbose_name="Дата завершения"
    )
    customer = models.CharField(max_length=255, blank=True, verbose_name="Заказчик")
    comment = models.TextField(blank=True, verbose_name="Примечание")

    def __str__(self):
        return f"Заказ по СЗ №{self.number_bn} от {self.date_created}"

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-date_created"]


class TrackingTable(models.Model):
    """Модель главной таблицы Отслеживание."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tracking_table",
        verbose_name="Заказ",
    )
    internal_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Внутренний номер"
    )
    product = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="Наименование и номер номенклатуры",
    )
    quantity = models.PositiveIntegerField(
        default=1, blank=True, null=True, verbose_name="Количество"
    )
    date_shipment = models.DateField(
        blank=True, null=True, verbose_name="Дата отгрузки"
    )
    date_entry_1c = models.DateField(
        blank=True, null=True, verbose_name="Дата занесения в 1С"
    )
    date_transfer_to_pdd = models.DateField(
        blank=True, null=True, verbose_name="Дата передачи СЗ в ПДО"
    )
    pps_cp = models.CharField(
        max_length=9, choices=PPS_CP_STATUS, default="not_need", verbose_name="РТК+УП"
    )
    order_number_1c = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Номер заказа в 1С"
    )
    date_transfer_to_ss = models.DateField(
        blank=True, null=True, verbose_name="Дата передачи СЗ в службу снабжения"
    )
    date_warehouse = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата поступления на склад заготовок, металла",
    )
    date_tentative_supply = models.DateField(
        blank=True,
        null=True,
        verbose_name="Предварительные сроки поставки заготовок, металла",
    )
    status_product = models.CharField(
        max_length=15,
        choices=PRODUCTION_STATUS,
        default="start",
        verbose_name="Статус производства",
    )
    date_completion = models.DateField(
        blank=True, null=True, verbose_name="Дата завершения"
    )
    comment = models.TextField(blank=True, null=True, verbose_name="Примечание")

    def __str__(self):
        return f"Позиция {self.product} для {self.order}"

    class Meta:
        verbose_name = "Позиция отслеживания"
        verbose_name_plural = "Главная таблица отслеживания"
        ordering = ["order", "product"]
