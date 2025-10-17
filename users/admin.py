from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = (
        "username",
        "last_name",
        "first_name",
        "patronymic",
        "position",
        "service_number",
    )
    list_filter = ("position", "groups")
    search_fields = (
        "last_name",
        "first_name",
        "patronymic",
        "position",
        "service_number",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Дополнительная информация",
            {
                "fields": (
                    "patronymic",
                    "service_number",
                    "internal_phone",
                    "mobile_phone",
                    "position",
                    "birthday",
                    "date_employment",
                    "date_dismissal",
                    "comment",
                )
            },
        ),
    )
