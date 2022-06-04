from django.urls import path

from authapp import views
from authapp.apps import AuthappConfig

app_name = AuthappConfig.name

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name='login'),
    path("register/", views.RegisterView.as_view(), name='register'),
    path("logout/", views.LogoutView.as_view(), name='logout'),
    path("profile_edit/", views.ProfileEditView.as_view(), name='profile_edit'),
]