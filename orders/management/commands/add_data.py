from django.core.management import call_command
from django.core.management.base import BaseCommand

from orders.models import Order, TrackingTable


class Command(BaseCommand):
    help = "Загрузка данных о пользователях из фикстур."

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        TrackingTable.objects.all().delete()
        Order.objects.all().delete()

        # Загружаем данные из фикстуры orders-trackingtable_fixture.json
        call_command("loaddata", "orders-trackingtable_fixture.json")
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully loaded ORDERS and TRACKINGTABLE from fixture!"
            )
        )
