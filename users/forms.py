from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.contrib.auth.models import Group

from orders.forms import StyleFormMixin

from .models import Employee


class CustomAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        """Преобразуем 'Иванов И. И.' в 'ИвановИ.И.'"""
        # Это необходимо так как username не может содержать пробелы
        return self.cleaned_data["username"].replace(" ", "")


class EmployeeCreationForm(StyleFormMixin, UserCreationForm):
    """Форма создания нового пользователя."""

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
        label="Группа пользователя",
        empty_label=None,
    )

    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = [
            "username",
            "last_name",
            "first_name",
            "patronymic",
            "service_number",
            "internal_phone",
            "mobile_phone",
            "email",
            "position",
            "birthday",
            "date_employment",
            "comment",
        ]

        help_texts = {
            "username": "Это поле используется для входа в систему. Пишите в формате ИвановИ.И. (без пробелов)",
        }

    def save(self, commit=True):
        # Сохраняем пользователя и присваеваем ему группу
        user = super().save(commit=False)

        if commit:
            user.save()

            # Добавляем пользователя в выбранную группу
            selected_group = self.cleaned_data["group"]
            user.groups.add(selected_group)

        return user


class EmployeeUpdateForm(StyleFormMixin, UserChangeForm):
    """Форма обновления данных пользователя."""

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
        label="Группа пользователя",
        empty_label=None,
    )

    class Meta:
        model = Employee
        fields = [
            "username",
            "last_name",
            "first_name",
            "patronymic",
            "service_number",
            "internal_phone",
            "mobile_phone",
            "email",
            "position",
            "birthday",
            "date_employment",
            "date_dismissal",
            "comment",
        ]
        help_texts = {
            "username": "Это поле используется для входа в систему. Пишите в формате ИвановИ.И. (без пробелов)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Убираем поле пароля
        if "password" in self.fields:
            del self.fields["password"]

        # Устанавливаем текущую группу пользователя
        if self.instance and self.instance.pk:
            user_groups = self.instance.groups.all()
            if user_groups:
                self.fields["group"].initial = user_groups.first()

    def save(self, commit=True):
        user = super().save(commit=False)

        # Логика для поля увольнения date_dismissal (установка is_active=False)
        date_dismissal = self.cleaned_data.get("date_dismissal")
        if date_dismissal:
            # Если установлена дата увольнения - деактивируем пользователя
            user.is_active = False
        else:
            # Если дата увольнения очищена - активируем пользователя
            user.is_active = True

        if commit:
            user.save()

            # Обновляем группу пользователя
            selected_group = self.cleaned_data["group"]
            user.groups.clear()
            user.groups.add(selected_group)

        return user
