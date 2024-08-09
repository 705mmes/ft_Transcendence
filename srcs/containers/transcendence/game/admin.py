from django.contrib import admin
from .models import GameHistory


class GameHistoryAdmin(admin.ModelAdmin):
    list_display = ('History1', 'Score1', 'History2', 'Score2')


admin.site.register(GameHistory, GameHistoryAdmin)
