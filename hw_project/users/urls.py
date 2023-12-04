from django.urls import path, include
from .views import RegisterView, LoginView, AddAuthorView

app_name = "users"

urlpatterns = [
    #path("", include("users.urls")),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    #path("add_author/", AddAuthorView.as_view(), name="add_author"),
    ]

