from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserView


urlpatterns = [
    path('users/', UserView.as_view(),name="Users-list"),
    # path('api/', include(router.urls)),
]
