from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView
from .models import Order, TrackingTable

from .forms import TrackingTableFieldForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

@login_required
def manager_orders(request):
    """Страница заказов для менеджера"""
    # Показываем только заказы текущего менеджера
    orders = Order.objects.filter(responsible=request.user)
    return render(request, 'orders/manager_orders.html', {
        'orders': orders,
    })

@login_required
def tracking_table(request):
    """Главная таблица отслеживания для всех остальных групп"""
    tracking_data = TrackingTable.objects.all()
    return render(request, 'orders/tracking_table.html', {
        'tracking_data': tracking_data,
        'title': 'Главная таблица отслеживания'
    })


class FieldUpdateView(LoginRequiredMixin, UpdateView):
    model = TrackingTable
    form_class = TrackingTableFieldForm
    template_name = 'orders/field_edit.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['field_name'] = self.kwargs['field_name']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['field_name'] = self.kwargs['field_name']
        context['field_verbose_name'] = self._get_field_verbose_name()
        return context

    def _get_field_verbose_name(self):
        """Получаем человеко-читаемое название поля"""
        field = self.model._meta.get_field(self.kwargs['field_name'])
        return field.verbose_name

    # def form_valid(self, form):
    #     return super().form_valid(form)

    # def form_valid(self, form):
    #     print(f"Форма валидна. Сохраняем поле: {self.kwargs['field_name']}")
    #     print(f"Данные формы: {form.cleaned_data}")
    #     response = super().form_valid(form)
    #     print("Объект сохранен!")
    #     return response

    def form_valid(self, form):
        print(f"Форма валидна. Сохраняем поле: {self.kwargs['field_name']}")
        print(f"Данные формы: {form.cleaned_data}")

        # СОХРАНЯЕМ ВРУЧНУЮ, чтобы убедиться, что данные записываются
        field_name = self.kwargs['field_name']
        new_value = form.cleaned_data[field_name]

        # Получаем объект и обновляем поле
        obj = form.save(commit=False)
        setattr(obj, field_name, new_value)
        obj.save()

        print(f"Объект сохранен! Новое значение: {getattr(obj, field_name)}")

        return super().form_valid(form)

    def get_success_url(self):
        # Четко указываем URL для редиректа после успешного сохранения
        return reverse('tracking_table')

    def dispatch(self, request, *args, **kwargs):
        # Проверяем права доступа к полю
        if not self._has_edit_permission():
            from django.contrib import messages
            messages.error(request, 'У вас нет прав для редактирования этого поля')
            return redirect('tracking_table')
        return super().dispatch(request, *args, **kwargs)

    def _has_edit_permission(self):
        """Проверяем права на редактирование конкретного поля"""
        user = self.request.user
        field_name = self.kwargs['field_name']

        if user.groups.filter(name='directors').exists():
            return True

        # Проверяем права для каждой группы
        if field_name in ['internal_number', 'product', 'quantity', 'date_shipment']:
            return user.groups.filter(name='process_engineer').exists()

        if field_name in ['date_entry_1c', 'date_transfer_to_pdd', 'order_number_1c']:
            return user.groups.filter(name='plan_disp_department').exists()

        if field_name in ['date_tentative_supply']:
            return user.groups.filter(name='supply_service').exists()

        return False

#В будущем для подобных случаев лучше использовать modelform_factory - он создает "чистые" формы без наследования и динамических изменений.

# Теперь ваша ERP-система полноценно работает с редактированием данных!
#
#В будущем для подобных случаев лучше использовать modelform_factory - он создает "чистые" формы без наследования и динамических изменений.


# 3. Альтернативный подход - используем forms.modelform_factory (более надежный):
# Если вышеуказанное не сработает, замените форму и представление на это:
# from django.forms import modelform_factory
# from django.db import models
#
#
# class FieldUpdateView(LoginRequiredMixin, UpdateView):
#     model = TrackingTable
#     template_name = 'orders/field_edit.html'
#
#     def get_form_class(self):
#         field_name = self.kwargs['field_name']
#
#         # Определяем виджет в зависимости от типа поля
#         model_field = TrackingTable._meta.get_field(field_name)
#         widgets = {}
#
#         if isinstance(model_field, models.DateField):
#             widgets[field_name] = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
#         else:
#             widgets[field_name] = forms.TextInput(attrs={'class': 'form-control'})
#
#         # Создаем форму с одним полем
#         return modelform_factory(
#             TrackingTable,
#             fields=(field_name,),
#             widgets=widgets
#         )
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['field_name'] = self.kwargs['field_name']
#         context['field_verbose_name'] = self._get_field_verbose_name()
#         return context
#
#     def _get_field_verbose_name(self):
#         field = self.model._meta.get_field(self.kwargs['field_name'])
#         return field.verbose_name
#
#     def form_valid(self, form):
#         print(f"Сохранение поля: {self.kwargs['field_name']}")
#         print(f"Новое значение: {form.cleaned_data}")
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse('tracking_table')
#
#     # ... остальные методы без изменений ...