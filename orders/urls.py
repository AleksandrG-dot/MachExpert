from django.urls import path

from .views import (FieldUpdateView, OrderCreateView, manager_orders,
                    tracking_table)

# app_name = OrdersConfig.name

urlpatterns = [
    path("manager/", manager_orders, name="manager_orders"),
    path("tracking/", tracking_table, name="tracking_table"),
    path(
        "tracking/<int:pk>/edit/<str:field_name>/",
        FieldUpdateView.as_view(),
        name="edit_field",
    ),
]
