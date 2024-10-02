from django.contrib import admin
from .models import GameHistory, GameLobby, TournamentLobby


class GameHistoryAdmin(admin.ModelAdmin):
    list_display = ('History1', 'Score1', 'History2', 'Score2')

class GameLobbyAdmin(admin.ModelAdmin):
    list_display = ('Player1', 'Player2')

class TournamentLobbyAdmin(admin.ModelAdmin):
    list_display = ('P1', 'P2', 'P3', 'P4')

admin.site.register(GameHistory, GameHistoryAdmin)
admin.site.register(TournamentLobby, TournamentLobbyAdmin)
admin.site.register(GameLobby, GameLobbyAdmin)

