from django.contrib import admin

# Register your models here.
# listings/admin.py
from authentication.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_connected')


admin.site.register(User, UserAdmin)