from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from .views import home_redirect, EmployeesListView

# app_name = UsersConfig.name

urlpatterns = [
    path("", home_redirect, name="home"),
    path(
        "login/",
        LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("employees/", EmployeesListView.as_view(), name="employees_list"),
]
