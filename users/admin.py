from django.contrib import admin
from .models import Users, UserRoles

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email')
    list_filter = ('role',)

@admin.register(UserRoles)
class UserRolesAdmin(admin.ModelAdmin):
    list_display = ('role_name',)