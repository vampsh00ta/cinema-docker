from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from .forms import UserAdminCreationForm, UserAdminChangeForm

from .models import *

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm


    list_display = ['email','username', 'firstName', 'secondName','is_active', 'admin']
    list_filter = ['admin']
    fieldsets = (
        (None, {'fields': ('email','username','password','firstName','secondName','is_active')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'account_type')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'admin', 'firstName', 'secondName')}
         ),
    )
    search_fields = ['email', 'username']
    ordering = ['email', 'username']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Film)
admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Serial)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(Trailer)

