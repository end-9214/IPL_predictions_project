# Generated by Django 5.2 on 2025-05-05 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Match",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("team1", models.CharField(max_length=50)),
                ("team2", models.CharField(max_length=50)),
                ("venue", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Predictions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("team1", models.CharField(max_length=50)),
                ("team2", models.CharField(max_length=50)),
                ("venue", models.CharField(max_length=100)),
                ("predicted_winner", models.CharField(max_length=50)),
                ("team1_win_rate", models.FloatField()),
                ("team2_win_rate", models.FloatField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="TeamWinrates",
            fields=[
                (
                    "team",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("home_win_percentage", models.FloatField()),
                ("away_win_percentage", models.FloatField()),
            ],
        ),
    ]
