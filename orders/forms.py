from django import forms

from .models import Order, TrackingTable


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["number_bn", "customer", "amount", "folder_bn", "comment"]
        widgets = {
            "number_bn": forms.TextInput(attrs={"class": "form-control"}),
            "customer": forms.TextInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "folder_bn": forms.URLInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class TrackingTableFieldForm(forms.ModelForm):
    class Meta:
        model = TrackingTable
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
