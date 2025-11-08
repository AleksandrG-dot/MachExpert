from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from users.forms import (CustomAuthenticationForm, EmployeeCreationForm,
                         EmployeeUpdateForm)
from users.models import Employee


class HRRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Миксин для проверки прав доступа - только отдел кадров"""

    def test_func(self):
        return self.request.user.groups.filter(name="hr_department").exists()


class CustomLoginView(LoginView):
    """Кастомный контроллер логирования. С удалением пробелов в username в форме."""

    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"


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
    template_name = "users/employees_list.html"
    context_object_name = "employees"

    def get_queryset(self):
        """Формирования списка сотрудников в зависимости от группы пользователя."""
        user = self.request.user

        if user.groups.filter(name="hr_department").exists():
            return self.model.objects.all().order_by("last_name", "first_name")

        # Показываем только сотрудников, которые не уволены
        return Employee.objects.filter(is_active=True).order_by(
            "is_active", "last_name", "first_name"
        )


class EmployeeCreateView(HRRequiredMixin, CreateView):
    """Класс для создания(регистрации) нового сотрудника (пользователя системы)."""

    model = Employee
    form_class = EmployeeCreationForm
    template_name = "users/employee_form.html"
    success_url = reverse_lazy("employees_list")


class EmployeeUpdateView(HRRequiredMixin, UpdateView):
    """Класс для редактирования данных сотрудника (пользователя системы)."""

    model = Employee
    form_class = EmployeeUpdateForm
    template_name = "users/employee_form.html"
    success_url = reverse_lazy("employees_list")


class EmployeeDeleteView(HRRequiredMixin, DeleteView):
    """Класс для удаления сотрудника (пользователя системы)."""

    model = Employee
    template_name = "users/employee_confirm_delete.html"
    success_url = reverse_lazy("employees_list")
