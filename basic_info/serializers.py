from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from rest_framework.response import Response
from .models import *
from .views import *


class PlayerStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PlayerStats
        fields = '__all__'  

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
        

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name','logo','club_state')

class TeamPlayerSerializer(serializers.ModelSerializer):
    team_player = PlayerSerializer(many=True,read_only=True)

    class Meta:
        model = Team
        fields = ('name', 'logo', 'team_player')

class MatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Matches
        fields = ('venue','date')

class MatchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model =  MatchResult
        fields = ('match','winner')   

class PointsTableSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PointsTable
        fields = '__all__'






        


