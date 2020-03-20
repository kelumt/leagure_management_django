from django.contrib import admin

from .models import Coach, Player, LeagueAdmin, Team, Game, GamePlayer, LoginTracker

# Register your models here.

admin.site.register(Coach)
admin.site.register(Player)
admin.site.register(LeagueAdmin)
admin.site.register(Team)
admin.site.register(Game)
admin.site.register(GamePlayer)
admin.site.register(LoginTracker)
