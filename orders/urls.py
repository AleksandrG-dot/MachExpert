from django.urls import path

from .views import (FieldUpdateView, ManagersReportView, OrderCreateView,
                    OrderDeleteView, OrderDetailView, OrderUpdateView,
                    TrackingTableCreateView, manager_orders, tracking_table)

urlpatterns = [
    path("manager/", manager_orders, name="manager_orders"),
    path("tracking/", tracking_table, name="tracking_table"),
    path(
        "tracking/<int:pk>/edit/<str:field_name>/",
        FieldUpdateView.as_view(),
        name="edit_field",
    ),
    path("order/create/", OrderCreateView.as_view(), name="order_create"),
    path("order/<int:pk>/detail/", OrderDetailView.as_view(), name="order_detail"),
    path("order/<int:pk>/edit/", OrderUpdateView.as_view(), name="order_edit"),
    path("order/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("tracking/add/", TrackingTableCreateView.as_view(), name="tracking_add"),
    path("reports/managers/", ManagersReportView.as_view(), name="managers_report"),
]
