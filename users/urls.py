from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (CustomLoginView, EmployeeCreateView, EmployeeDeleteView,
                    EmployeesListView, EmployeeUpdateView, home_redirect)

# app_name = UsersConfig.name

urlpatterns = [
    path("", home_redirect, name="home"),
    path(
        "login/",
        CustomLoginView.as_view(),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("employees/", EmployeesListView.as_view(), name="employees_list"),
    path("employees/create/", EmployeeCreateView.as_view(), name="employee_create"),
    path(
        "employees/<int:pk>/edit/", EmployeeUpdateView.as_view(), name="employee_edit"
    ),
    path(
        "employees/<int:pk>/delete/",
        EmployeeDeleteView.as_view(),
        name="employee_delete",
    ),
]
