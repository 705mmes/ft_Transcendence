from django.contrib import admin

# Register your models here.
# listings/admin.py
from authentication.models import User

admin.site.register(User)