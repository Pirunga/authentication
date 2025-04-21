
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Here you have to import the User model from your app!
from authapi.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
        model = CustomUser
        list_display = ('first_name', 'last_name', 'email',)
        list_filter = ('first_name', 'last_name', 'email',)
        search_fields = ('first_name', 'last_name', 'email',)
        ordering = ('first_name', 'last_name', 'email',)
        fieldsets = (
            (None, {'fields': ('email', 'password')}),
            ('Personal info', {'fields': ('first_name', 'last_name')}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
            ('Important dates', {'fields': ('last_login',)}),
        )
