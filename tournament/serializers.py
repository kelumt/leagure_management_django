from rest_framework import serializers
from .models import Player, Team, Coach, Game, GamePlayer, LoginTracker

class CoachSerialzerNested(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = ('id', 'username', 'first_name', 'last_name')

class TeamSerializerNested(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name')

class PlayerSerializer(serializers.ModelSerializer):
    playing_team = TeamSerializerNested()

    class Meta:
        model = Player
        fields = ('id', 'username', 'first_name', 'last_name', 'height', 'playing_team', 'number_of_games', 'average_score')

class PlayerSerializerNested(serializers.ModelSerializer):        
    class Meta:
        model = Player
        fields = ('id', 'username', 'first_name', 'last_name', 'height')

class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializerNested(many=True, read_only=True)
    coach_for_team = CoachSerialzerNested(read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'coach_for_team', 'players', 'num_of_players', 'average_score')

class CoachSerialzer(serializers.ModelSerializer):
    team = TeamSerializerNested()

    class Meta:
        model = Coach
        fields = ('id', 'username', 'first_name', 'last_name', 'team')     



class GamePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePlayer
        fields = ('player', 'game', 'score')

class GamePlayerSerializerNested(serializers.ModelSerializer):
    player = PlayerSerializerNested()

    class Meta:
        model = GamePlayer
        fields = ('player', 'score')

class GameSerializer(serializers.ModelSerializer):
    home_team = TeamSerializerNested()
    away_team = TeamSerializerNested()

    class Meta:
        model = Game
        fields = ('id', 'home_team', 'away_team', 'home_team_score', 'away_team_score', 'date', 'stadium')

class LoginTrackerSeralizer(serializers.ModelSerializer):
    class Meta: 
        model = LoginTracker
        fields = '__all__'





