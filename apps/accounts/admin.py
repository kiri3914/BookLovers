from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('phone_number',  'bio', 'birthdate')
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name','email', 'username', 'phone_number',  'bio', 'birthdate', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name', 'last_name','email', 'username', 'phone_number',  'bio', 'birthdate', 'password1', 'password2')}
         ),
    )
    search_fields = ('username', 'phone_number', 'birthdate', 'bio', 'email')
    ordering = ('username', 'phone_number', 'birthdate')


admin.site.register(CustomUser, CustomUserAdmin)
