from django.urls import path

from .apps import OrdersConfig
from .views import manager_orders, tracking_table, FieldUpdateView

# app_name = OrdersConfig.name

urlpatterns = [
    path('manager/', manager_orders, name='manager_orders'),
    path('tracking/', tracking_table, name='tracking_table'),

    path('tracking/<int:pk>/edit/<str:field_name>/', FieldUpdateView.as_view(), name='edit_field'),
]