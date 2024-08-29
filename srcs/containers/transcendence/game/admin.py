from django.contrib import admin
from .models import GameHistory, GameLobby, PosPlayer


class GameHistoryAdmin(admin.ModelAdmin):
    list_display = ('History1', 'Score1', 'History2', 'Score2')

class GameLobbyAdmin(admin.ModelAdmin):
    list_display = ('Player1', 'Player2')

class GamePosPlayer(admin.ModelAdmin):
    list_display = ('Player', 'posX', 'posY')

admin.site.register(GameHistory, GameHistoryAdmin)
admin.site.register(GameLobby, GameLobbyAdmin)
admin.site.register(PosPlayer, GamePosPlayer)
