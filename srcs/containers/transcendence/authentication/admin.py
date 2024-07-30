from django.contrib import admin

# Register your models here.
# listings/admin.py
from authentication.models import User, FriendList


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_connected')


class FriendListAdmin(admin.ModelAdmin):
    list_display = ()


admin.site.register(User, UserAdmin)
admin.site.register(FriendList, FriendListAdmin)