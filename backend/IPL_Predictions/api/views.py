import csv
from django import views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Match, TeamWinrates, Predictions
from .serializers import MatchSerializer, WinratesSerializer
from IPL_SCORE_WINNER_PREDICTION_MODEL.predict import predict_ipl_match
from datetime import date, datetime



class UploadMatchesAPIView(APIView):
    def post(self, request, *args, **kwargs):
        file_path = "scraper/ipl_matches.csv"
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                match_data = {
                    "date": datetime.strptime(row["date"], "%d-%m-%Y").strftime("%Y-%m-%d"),
                    "team1": row["team1"],
                    "team2": row["team2"],
                    "venue": row["venue"],
                }
                serializer = MatchSerializer(data=match_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        winrates_file_path = "scraper/teamwise_home_and_away.csv"
        with open(winrates_file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                winrate_data = {
                    "team": row["team"],
                    "home_win_percentage": float(row["home_win_percentage"]),
                    "away_win_percentage": float(row["away_win_percentage"]),
                }
                serializer = WinratesSerializer(data=winrate_data)
                if serializer.is_valid():
                    serializer.save()

        return Response(
            {"message": "Matches and win rates uploaded successfully!"},
            status=status.HTTP_200_OK,
        )


class CurrentPredictionsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        today = date.today()
        matches = Match.objects.filter(date=today)

        if not matches.exists():
            return Response(
                {"message": "No matches scheduled for today."},
                status=status.HTTP_404_NOT_FOUND,
            )

        predictions = []

        for match in matches:
            team1 = match.team1
            team2 = match.team2
            venue = match.venue

            team1_win_rate = TeamWinrates.objects.get(team=team1).home_win_percentage / 100
            team2_win_rate = TeamWinrates.objects.get(team=team2).away_win_percentage / 100
            scenarios = [
                {"toss_winner": team1, "toss_decision": "bat"},
                {"toss_winner": team1, "toss_decision": "field"},
                {"toss_winner": team2, "toss_decision": "bat"},
                {"toss_winner": team2, "toss_decision": "field"},
            ]

            for scenario in scenarios:
                toss_winner = scenario["toss_winner"]
                toss_decision = scenario["toss_decision"]

                winning_team, probability = predict_ipl_match(
                    team1=team1,
                    team2=team2,
                    venue=venue,
                    toss_winner=toss_winner,
                    toss_decision=toss_decision,
                    team1_win_rate=team1_win_rate,
                    team2_win_rate=team2_win_rate,
                )

                predictions.append(
                    {
                        "match": f"{team1} vs {team2}",
                        "venue": venue,
                        "toss_winner": toss_winner,
                        "toss_decision": toss_decision,
                        "predicted_winner": winning_team,
                        "win_probability": round(probability * 100, 2),
                    }
                )

        return Response(predictions, status=status.HTTP_200_OK)
    
