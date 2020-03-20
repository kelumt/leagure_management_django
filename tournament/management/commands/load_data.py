from django.core.management.base import BaseCommand, CommandError
from django.db.models.base import ObjectDoesNotExist
from django.contrib.auth.models import User
from tournament.models import LeagueAdmin, Coach, Player, Team, Game, GamePlayer
import datetime

class Command(BaseCommand):
    help = 'Load initial users(League Admins, Coaches, Players) for the system.'

    def handle(self, **options):        

        try:
           # create a super user
           super_user = self.createSuperUser('super', 'Super', 'User', '1234')

           # create league admin 
           league_admin = self.createLeagueAdmin('leagueadmin', 'League', 'Admin', '1234')
           
           # create coaches
           coach1 = self.createCoach('coach1', 'Coach', 'One', '1234')
           coach2 = self.createCoach('coach2', 'Coach', 'Two', '1234')

           team1 = self.createTeam('Atlanta Hawks', coach1)
           team2 = self.createTeam('Golden State Warriors', coach2)

           # players for team1
           player1 = self.createPlayer('adamss', 'Adams', 'Steven', '1234', 1.23, team1)
           player2 = self.createPlayer('allenj', 'Allen', 'Jarrett', '1234', 1.23, team1)
           player3 = self.createPlayer('bonej', 'Bone', 'Jordan', '1234', 1.23, team1)
           player4 = self.createPlayer('cookq', 'Cook', 'Quinn', '1234', 1.23, team1)

           # players for team2
           player5 = self.createPlayer('fallt', 'Fall', 'Tacko', '1234', 1.23, team2)
           player6 = self.createPlayer('frazierm', 'Frazier', 'Michael', '1234', 1.23, team2)
           player7 = self.createPlayer('johnsont', 'Johnson', 'Tyler', '1234', 1.23, team2)
           player8 = self.createPlayer('motleyj', 'Motley', 'Johnathan', '1234', 1.23, team2)

           # create games
           game1 = self.createGame(team1, team2, 80, 112, datetime.datetime(2020, 1, 10, 16, 0, 0), 'State Farm Arena')
           game2 = self.createGame(team2, team1, 77, 119, datetime.datetime(2020, 2, 5, 18, 0, 0), 'Chase Center')

           # create game players

           # players for game1 for team1 
           game_player1 = self.createGamePlayer(game1, player1, 12)
           game_player2 = self.createGamePlayer(game1, player2, 9)

           # players for game1 for team2 
           game_player3 = self.createGamePlayer(game1, player5, 33)
           game_player4 = self.createGamePlayer(game1, player6, 1)

           # players for game2 for team1 
           game_player5 = self.createGamePlayer(game2, player1, 17)
           game_player6 = self.createGamePlayer(game2, player2, 3)

           # players for game2 for team2 
           game_player7 = self.createGamePlayer(game2, player5, 23)
           game_player8 = self.createGamePlayer(game2, player8, 9)

        except ValueError as error:
            raise CommandError(str(error))



    def createUser(self, user_name, first_name, last_name, password):
        user = User.objects.create_user(user_name, password=password, first_name=first_name, last_name=last_name)
        return user

    def createSuperUser(self, user_name, first_name, last_name, password):
        super_user = User.objects.create_superuser(user_name, password=password, first_name=first_name, last_name=last_name)
        return super_user

    def createLeagueAdmin(self, user_name, first_name, last_name, password):
        league_admin = LeagueAdmin.objects.create(username=user_name, password=password, first_name=first_name, last_name=last_name)
        return league_admin

    def createCoach(self, user_name, first_name, last_name, password):
        coach = Coach.objects.create(username=user_name, password=password, first_name=first_name, last_name=last_name)
        return coach

    def createPlayer(self, user_name, first_name, last_name, password, height, team):
        player = Player.objects.create(username=user_name, password=password, first_name=first_name, last_name=last_name, height=height, playing_team=team)
        return player

    def createTeam(self, name, coach):
        team = Team.objects.create(name=name, coach_for_team=coach)
        return team

    def createGame(self, home_team, away_team, home_team_score, away_team_score, date, stadium):
        game = Game.objects.create(home_team=home_team, away_team=away_team, home_team_score=home_team_score, away_team_score=away_team_score, date=date, stadium=stadium)
        return game

    def createGamePlayer(self, game, player, score):
        game_player = GamePlayer.objects.create(player=player, game=game, score=score)
        return game_player

