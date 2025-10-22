from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import OrderForm, TrackingTableFieldForm, TrackingTableForm
from .models import Order, TrackingTable


@login_required
def manager_orders(request):
    """Функция для просмотра Страницы заказов. Для менеджера - только его заказы, для других групп - все заказы"""

    # Проверяем принадлежность пользователя к группам, которым доступны все заказы
    if (
        request.user.groups.filter(
            name__in=[
                "directors",
                "process_engineer",
                "plan_disp_department",
                "supply_service",
            ]
        ).exists()
        or request.user.is_superuser
    ):
        # Показываем все заказы для директоров, инженеров, ПДО и службы снабжения
        orders = Order.objects.all()
    elif request.user.groups.filter(name="manager").exists():
        # Для менеджеров - только их собственные заказы
        orders = Order.objects.filter(responsible=request.user)

    # Cортировка
    # orders = orders.order_by('-created_at')

    return render(request, "orders/manager_orders.html", {"orders": orders})


class OrderDetailView(LoginRequiredMixin, DeleteView):
    model = Order
    form_class = OrderForm
    template_name = "orders/order_detail.html"
    success_url = reverse_lazy("manager_orders")


class OrderCreateView(LoginRequiredMixin, CreateView):
    """Класс для добавления нового заказа."""

    model = Order
    form_class = OrderForm
    template_name = "orders/order_form.html"
    success_url = reverse_lazy("manager_orders")

    def form_valid(self, form):
        # Автоматически назначаем текущего пользователя как ответственного менеджера
        form.instance.responsible = self.request.user
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Класс для редактирования заказа."""

    model = Order
    form_class = OrderForm
    template_name = "orders/order_form.html"
    success_url = reverse_lazy("manager_orders")

    def test_func(self):
        """Проверяем, что заказ принадлежит пользователю и в статусе "created" """
        return (
            self.request.user == self.get_object().responsible
            and self.get_object().order_status == "created"
        )


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Класс для удаления заказа."""

    model = Order
    template_name = "orders/order_confirm_delete.html"
    success_url = reverse_lazy("manager_orders")

    def test_func(self):
        """Проверяем, что заказ принадлежит пользователю и в статусе "created" """
        return (
            self.request.user == self.get_object().responsible
            and self.get_object().order_status == "created"
        )


@login_required
def tracking_table(request):
    """Главная таблица 'Отслеживание'."""
    tracking_data = TrackingTable.objects.all()
    new_orders = Order.objects.filter(order_status="created")
    return render(
        request,
        "orders/tracking_table.html",
        {
            "tracking_data": tracking_data,
            "new_orders": new_orders,
        },
    )


class FieldUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Класс редактирования одного поля таблицы TrackingTable. Данные название поля хранится в field_name."""

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
                "comment",
            ]

        if user.groups.filter(name="plan_disp_department").exists():
            return field_name in [
                "order_number_1c",
                "date_transfer_to_ss",
                "date_warehouse",
                "status_product",
                "comment",
            ]

        if user.groups.filter(name="supply_service").exists():
            return field_name in [
                "date_tentative_supply",
                "comment",
            ]

        return False

    def form_valid(self, form):
        # Сохраняем объект TrackingTable
        response = super().form_valid(form)

        # Далее выполняется проверка. Если поля status_product в таблице TrackingTable у всех записей, относящихся
        # к текущему заказу, в статусе completed, то устанавливаем поле order_status в Order в значение completed
        if form.has_changed() and "status_product" in form.changed_data:

            # Получаем обновленный объект TrackingTable
            tracking_record = self.object

            # Проверяем, изменилось ли поле status_product на 'completed'
            if tracking_record.status_product == "completed":
                # Получаем все записи TrackingTable для этого заказа
                order_records = TrackingTable.objects.filter(
                    order=tracking_record.order
                )

                # Проверяем, все ли записи имеют статус 'completed'
                all_completed = all(
                    record.status_product == "completed" for record in order_records
                )

                if all_completed:
                    # Меняем статус заказа на 'completed'
                    order = tracking_record.order
                    order.order_status = "completed"
                    order.save()

        return response


class TrackingTableCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Класс для добавления записей в таблицу TrackingTable."""

    model = TrackingTable
    form_class = TrackingTableForm
    template_name = "orders/trackingtable_form.html"
    success_url = reverse_lazy("tracking_table")

    def test_func(self):
        """Проверяем, что пользователь в нужных группах"""
        return (
            self.request.user.groups.filter(
                name__in=["process_engineer", "directors"]
            ).exists()
            or self.request.user.is_superuser
        )

    def form_valid(self, form):
        # Сохраняем запись отслеживания
        response = super().form_valid(form)

        # Меняем статус заказа на 'at_work'
        order = form.cleaned_data["order"]
        order.order_status = "at_work"
        order.save()

        return response
