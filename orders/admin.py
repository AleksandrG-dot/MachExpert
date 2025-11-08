from django.contrib import admin

from orders.models import Order, TrackingTable


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "number_bn",
        "responsible",
        "customer",
        "order_status",
        "date_created",
    )
    list_filter = ("order_status", "date_created", "responsible")
    search_fields = ("number_bn", "customer", "responsible__last_name")


@admin.register(TrackingTable)
class TrackingTableAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "internal_number",
        "product",
        "quantity",
        "date_shipment",
        "status_product",
    )
    list_filter = ("status_product", "pps_cp", "order__responsible")
    search_fields = ("product", "internal_number", "order__number_bn")
