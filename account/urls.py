from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_page, name="login_page"),
    path("register/", views.register, name="register"),
    path("activate/", views.activate_email, name="activate_email"),
    path("adminlogin/", views.admin_login, name="adminlogin"),
    path("logout/", views.logout_page, name="logout"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
]
