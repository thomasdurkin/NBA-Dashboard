from django.contrib import admin
from .models import Team, BoxScore, GameOdds, Player, PlayerOdds, PlayerStats

# Register your models here.
admin.site.register(Team)
admin.site.register(BoxScore)
admin.site.register(GameOdds)
admin.site.register(Player)
admin.site.register(PlayerOdds)
admin.site.register(PlayerStats)