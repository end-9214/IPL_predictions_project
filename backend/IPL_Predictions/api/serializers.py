from rest_framework import serializers
from .models import Match, TeamWinrates, Predictions


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ["date", "team1", "team2", "venue"]


class WinratesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamWinrates
        fields = ["team", "home_win_percentage", "away_win_percentage"]
