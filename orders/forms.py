# from django import forms
# from .models import TrackingTable
#
#
# class TrackingTableFieldForm(forms.ModelForm):
#     class Meta:
#         model = TrackingTable
#         fields = []  # Будем динамически определять
#
#     def __init__(self, *args, **kwargs):
#         field_name = kwargs.pop('field_name', None)
#         super().__init__(*args, **kwargs)
#
#         if field_name:
#             self.fields[field_name] = self._get_field(field_name)
#
#     def _get_field(self, field_name):
#         """Возвращает поле формы для указанного поля модели"""
#         field = self._meta.model._meta.get_field(field_name)
#         form_field = self.fields.get(field_name, forms.Field())
#
#         # Настраиваем поле в зависимости от типа
#         if isinstance(field, (forms.DateField,)):
#             form_field.widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
#         else:
#             form_field.widget = forms.TextInput(attrs={'class': 'form-control'})
#
#         return form_field


from django import forms
from django.db import models
from .models import TrackingTable


class TrackingTableFieldForm(forms.ModelForm):
    class Meta:
        model = TrackingTable
        fields = []  # Будем динамически определять

    def __init__(self, *args, **kwargs):
        field_name = kwargs.pop('field_name', None)
        super().__init__(*args, **kwargs)

        if field_name:
            # Создаем поле формы на основе поля модели
            model_field = TrackingTable._meta.get_field(field_name)
            form_field = model_field.formfield()

            # Настраиваем виджеты
            if isinstance(model_field, models.DateField):
                form_field.widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
            else:
                form_field.widget.attrs.update({'class': 'form-control'})

            self.fields[field_name] = form_field
            # КРИТИЧЕСКИ ВАЖНО: обновляем fields в Meta
            self._meta.fields = [field_name]


    # def __init__(self, *args, **kwargs):
    #     self.field_name = kwargs.pop('field_name', None)
    #     super().__init__(*args, **kwargs)
    #
    #     if self.field_name:
    #         # Динамически добавляем поле в форму
    #         self.fields[self.field_name] = self._create_form_field(self.field_name)
    #         # ОБЯЗАТЕЛЬНО обновляем Meta.fields
    #         self.Meta.fields = [self.field_name]
    #
    # def _create_form_field(self, field_name):
    #     """Создает поле формы на основе поля модели"""
    #     # Получаем поле из модели
    #     model_field = TrackingTable._meta.get_field(field_name)
    #
    #     # Используем встроенный метод для создания соответствующего поля формы
    #     form_field = model_field.formfield()
    #
    #     if form_field:
    #         # Настраиваем виджет в зависимости от типа поля
    #         if isinstance(form_field, forms.DateField):
    #             form_field.widget = forms.DateInput(attrs={
    #                 'type': 'date',
    #                 'class': 'form-control'
    #             })
    #         elif isinstance(form_field, (forms.IntegerField, forms.DecimalField)):
    #             form_field.widget.attrs.update({'class': 'form-control'})
    #         else:
    #             form_field.widget.attrs.update({'class': 'form-control'})
    #
    #     return form_field