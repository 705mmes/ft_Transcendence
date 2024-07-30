from django.contrib import admin

# Register your models here.
# listings/admin.py
from authentication.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_connected')


# class FriendListAdmin(admin.ModelAdmin):
    # list_display = ('user1', 'user2')


admin.site.register(User, UserAdmin)
# admin.site.register(FriendList, FriendListAdmin)