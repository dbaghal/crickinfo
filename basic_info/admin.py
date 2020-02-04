from django.contrib import admin
from .models import *

class PlayerAdmin(admin.TabularInline):
    model = Player
    extra = 0

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name','club_state','logo',)
    inlines      = (PlayerAdmin,)

class MatchesAdmin(admin.ModelAdmin):
    list_display = ('host_team','opponent_team','venue','date')

class MatchResultAdmin(admin.ModelAdmin):
    list_display = ('match','winner_name',)
    

class PointsTableAdmin(admin.ModelAdmin):
    list_display = ('team_name','matches','win','loss','points')
    ordering = ('-points',)


class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ('player','matches','runs','fifty','hundred','highest_score','wicket')

admin.site.register(Team,TeamAdmin)
admin.site.register(PlayerStats,PlayerStatsAdmin)
admin.site.register(Matches,MatchesAdmin)
admin.site.register(MatchResult,MatchResultAdmin)
admin.site.register(PointsTable,PointsTableAdmin)