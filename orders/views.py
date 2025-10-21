from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import OrderCreateForm, TrackingTableFieldForm
from .models import Order, TrackingTable


@login_required
def manager_orders(request):
    """Страница заказов для менеджера"""
    # Показываем только заказы текущего менеджера
    orders = Order.objects.filter(responsible=request.user)
    return render(
        request,
        "orders/manager_orders.html",
        {
            "orders": orders,
        },
    )


@login_required
def tracking_table(request):
    """Главная таблица отслеживания для всех остальных групп"""
    tracking_data = TrackingTable.objects.all()
    return render(
        request,
        "orders/tracking_table.html",
        {"tracking_data": tracking_data, "title": "Главная таблица отслеживания"},
    )


class FieldUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Класс редактирования одного поля таблицы. Данные название поля хранится в field_name."""

    model = TrackingTable
    template_name = "orders/field_edit.html"
    success_url = reverse_lazy("tracking_table")

    def get_form_class(self):
        """Переопределение класса формы в котором передаем имя поля для редактирования."""

        class DynamicForm(TrackingTableFieldForm):
            class Meta:
                model = TrackingTable
                fields = [self.kwargs["field_name"]]  # Укажите нужные поля

        return DynamicForm

    def test_func(self):
        """Проверяем права на редактирование конкретного поля. Заодно осуществляем
        валидацию введенного значения (если поступит не значение поля, а, SQL-injector)
        """
        user = self.request.user
        field_name = self.kwargs["field_name"]

        if user.groups.filter(name="directors").exists():
            return True

        # Проверяем права для каждой группы
        if user.groups.filter(name="process_engineer").exists():
            return field_name in [
                "order",
                "internal_number",
                "product",
                "quantity",
                "date_shipment",
                "date_entry_1c",
                "date_transfer_to_pdd",
                "pps_cp",
                "status_product",
            ]

        if user.groups.filter(name="plan_disp_department").exists():
            return field_name in [
                "order_number_1c",
                "date_transfer_to_ss",
                "date_warehouse",
                "status_product",
            ]

        if user.groups.filter(name="supply_service").exists():
            return field_name in ["date_tentative_supply"]

        return False
