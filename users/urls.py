from django.urls import path
from .views import UsersView,UserDetailsView,RegisterView,LoginView,LogoutView


urlpatterns = [
    path('users/', UsersView.as_view(),name="Lists-All-Users"),
    path('user/<int:pk>', UserDetailsView.as_view(),name="User-details"),
    path('register/',RegisterView.as_view(), name="Register-New-User"),
    path('login/', LoginView.as_view(),name="Login"),
    path('logout/', LogoutView.as_view(),name="Logout"),
]
