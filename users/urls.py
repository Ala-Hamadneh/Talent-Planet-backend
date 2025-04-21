from django.urls import path
from .views import UsersView,LoginView


urlpatterns = [
    path('users/', UsersView.as_view(),name="Lists-All-Users"),
    path('user/<int:pk>', UsersView.as_view(),name="User-details"),
    path('users/register/',UsersView.as_view(), name="Register-New-User"),
    path('login/', LoginView.as_view(),name="Login"),
]
