from django.db import models


class Match(models.Model):
    date = models.DateField()
    team1 = models.CharField(max_length=50)
    team2 = models.CharField(max_length=50)
    venue = models.CharField(max_length=100)


class TeamWinrates(models.Model):
    team = models.CharField(max_length=50, primary_key=True)
    home_win_percentage = models.FloatField()
    away_win_percentage = models.FloatField()


class Predictions(models.Model):
    date = models.DateField()
    team1 = models.CharField(max_length=50)
    team2 = models.CharField(max_length=50)
    venue = models.CharField(max_length=100)
    predicted_winner = models.CharField(max_length=50)
    team1_win_rate = models.FloatField()
    team2_win_rate = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
