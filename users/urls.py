from django.urls import path
from .views import CreateUserView, CreateAuthTokenView, LogoutView


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("auth-token/", CreateAuthTokenView.as_view(), name="auth-token"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
