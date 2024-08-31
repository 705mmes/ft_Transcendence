from django.contrib import admin
from .models import GameHistory, GameLobby


class GameHistoryAdmin(admin.ModelAdmin):
    list_display = ('History1', 'Score1', 'History2', 'Score2')


class GameLobbyAdmin(admin.ModelAdmin):
    list_display = ('Player1', 'Player2')


admin.site.register(GameHistory, GameHistoryAdmin)
admin.site.register(GameLobby, GameLobbyAdmin)

