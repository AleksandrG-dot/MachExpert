from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView

from users.models import Employee


@login_required
def home_redirect(request):
    """Редирект пользователя на его рабочую страницу после логина"""
    user = request.user

    if user.groups.filter(name="hr_department").exists():
        return redirect("employees_list")  # Список сотрудников для кадров
    elif user.groups.filter(name="manager").exists():
        return redirect("manager_orders")  # Заказы менеджера для менеджеров
    else:
        return redirect("tracking_table")  # Главная таблица для остальных групп


class EmployeesListView(LoginRequiredMixin, ListView):
    """Класс для отображения списка сотрудников."""

    model = Employee
    template_name = "users/employees.html"
    context_object_name = "employees"

    def get_queryset(self):
        """Формирования списка сотрудников в зависимости от группы пользователя."""
        user = self.request.user

        if user.groups.filter(name="hr_department").exists():
            return self.model.objects.all()

        # Показываем только сотрудников, которые не уволены
        return Employee.objects.filter(date_dismissal__isnull=True)
