from django.contrib.auth.models import User
from django.db import models
from django.db.models import Case, F, Q, When

# Create your models here.

class LeagueAdmin(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)

class Coach(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)

class Team(models.Model):
    name = models.CharField(max_length=100)
    coach_for_team = models.OneToOneField(Coach, on_delete=models.DO_NOTHING)

    @property
    def num_of_players(self):
        return self.players.count

    @property
    def average_score(self):
        qs_avg_score = Game.objects.filter(Q(home_team=self) | Q(away_team=self)).aggregate(avg_score=models.Avg(Case(When(home_team=self, then=F('home_team_score')), When(away_team=self, then=F('away_team_score')), default=0)))
        return qs_avg_score["avg_score"]

class Player(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    playing_team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)
    height = models.FloatField()

    def number_of_games(self):
        return GamePlayer.objects.filter(player=self).count()

    def average_score(self):
        qs_avg_score = GamePlayer.objects.filter(player=self).aggregate(avg_score=models.Avg(F('score')))
        return qs_avg_score["avg_score"]

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Game(models.Model):
    home_team = models.OneToOneField(Team, related_name='game_home_team', on_delete=models.DO_NOTHING)
    away_team = models.OneToOneField(Team, related_name='game_away_team', on_delete=models.DO_NOTHING)
    home_team_score = models.IntegerField()
    away_team_score = models.IntegerField()
    date = models.DateTimeField()
    stadium = models.CharField(max_length=200)

class GamePlayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name='game_players', on_delete=models.DO_NOTHING)
    score = models.IntegerField()

class LoginTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    session_key = models.CharField(max_length=200)
    login_date_time = models.DateTimeField()
    logout_date_time = models.DateTimeField(null=True)
