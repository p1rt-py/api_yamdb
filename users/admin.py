from django.contrib import admin

from .models import CustomUser


class UserAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ('pk', 'username', 'email', 'role')
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, UserAdmin)
