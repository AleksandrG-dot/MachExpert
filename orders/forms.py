from django import forms
from django.forms import BooleanField, DateField

from .models import Order, TrackingTable


class StyleFormMixin:
    """Миксин для стилизации формы."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field, DateField):
                field.widget = forms.DateInput(
                    attrs={"class": "form-control", "type": "date"}
                )
            else:
                field.widget.attrs["class"] = "form-control"


class TrackingTableFieldForm(forms.ModelForm):
    class Meta:
        model = TrackingTable
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class OrderForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Order
        fields = ["number_bn", "customer", "amount", "folder_bn", "comment"]
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Дополнительная информация",
                }
            ),
        }


class TrackingTableForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = TrackingTable
        fields = [
            "order",
            "internal_number",
            "product",
            "quantity",
            "date_shipment",
            "date_entry_1c",
            "date_transfer_to_pdd",
            "pps_cp",
            "comment",
        ]
        widgets = {
            "order": forms.Select(attrs={"class": "form-control"}),
            "pps_cp": forms.Select(attrs={"class": "form-control"}),
            "comment": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Комментарий"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Сортируем заказы по number_bn
        self.fields["order"].queryset = Order.objects.all().order_by("number_bn")
