import logging

import numpy as np
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, Count, Sum
from rest_framework import views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F, ExpressionWrapper, DurationField, Q

from .models import Coach, Game, GamePlayer, LoginTracker, Player, Team
from .serializers import (
    CoachSerialzer, GamePlayerSerializer, GameSerializer,
    LoginTrackerSeralizer, PlayerSerializer, TeamSerializer)

# Create your views here.


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(methods=['GET'], detail=True)
    def percentile_90_player(self, request, pk=None):

        # get the team
        teamId = pk
        team = Team.objects.get(id=teamId)

        # get the players list for the given team
        player_ids = team.players.values_list('id', flat=True)

        # average score set for the players
        player_avg_score_set = GamePlayer.objects.filter(player_id__in=player_ids).values('player').annotate(avg_score=Avg('score'))

        avg_score_array = []
        for player in player_avg_score_set: 
            avg_score_array.append(player['avg_score'])

        # Sorted array of average score
        avg_score_array_sorted = avg_score_array.copy()
        avg_score_array_sorted.sort() 

        # index for the 90th percentile
        percentile_90_index = avg_score_array.index(np.percentile(avg_score_array_sorted, 90, interpolation='nearest'))

        # player id for 90th percentile
        player_id_in_90_percentile = player_avg_score_set[percentile_90_index]['player']

        # player for 90th percentile
        player_in_90_percentile = Player.objects.get(pk=player_id_in_90_percentile)

        playerSerializer = PlayerSerializer(player_in_90_percentile)
        logging.debug(playerSerializer.data)

        return Response(playerSerializer.data)

class CoachViewSet(viewsets.ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerialzer

class GameViewset(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class LoginTrackerViewSet(viewsets.ModelViewSet):
    queryset = LoginTracker.objects.all()
    serializer_class = LoginTrackerSeralizer

    @action(detail=False)
    def logged_in_count_for_user(self, request, pk=None):
        user_id = self.request.query_params.get('user_id')
        user = User.objects.get(pk=user_id)
        num_of_sessions = LoginTracker.objects.filter(user=user).count()
        return Response({"num_of_sessions" : num_of_sessions})

    @action(detail=False)
    def total_amount_of_time_for_user(self, request, pk=None):
        user_id = self.request.query_params.get('user_id')
        user = User.objects.get(pk=user_id)
        total_amount_of_time = LoginTracker.objects.filter(user=user).annotate(diff=ExpressionWrapper(F('logout_date_time')-F('login_date_time'), output_field=DurationField())).aggregate(Sum('diff'))

        return Response({"total_amount_of_time" : total_amount_of_time})

    @action(detail=False)
    def online_user_list(self, request, pk=None):
        online_user_count = LoginTracker.objects.filter(logout_date_time__isnull=True).count()

        return Response({"online_user_count" : online_user_count})


