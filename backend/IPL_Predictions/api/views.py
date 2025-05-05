import csv
from django import views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Match, TeamWinrates, Predictions
from .serializers import MatchSerializer, WinratesSerializer
from IPL_SCORE_WINNER_PREDICTION_MODEL.predict import predict_ipl_match
from datetime import date, datetime
from llm.groq_llm import analyze_predictions, analyze_model_training
import subprocess
import json


class TrainModelOnDataAPIView(APIView):
    def get(self, request, *args, **kwargs):
        process = subprocess.run(
            ["python", "IPL_SCORE_WINNER_PREDICTION_MODEL/train_models.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if process.returncode != 0:
            return Response(
                {"message": "Model training failed!", "error": process.stderr},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        output_path = "IPL_SCORE_WINNER_PREDICTION_MODEL/saved_models/model_evaluation.json"
        with open(output_path, "r") as f:
            evaluation_output = json.load(f)

        insights = analyze_model_training(evaluation_output)
        return Response(
            {
                "message": "Model training completed successfully!",
                "output": evaluation_output,
                "insights": insights,
            },
            status=status.HTTP_200_OK,
        )



class UploadMatchesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        file_path = "scraper/ipl_matches.csv"
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                match_data = {
                    "date": datetime.strptime(row["date"], "%d-%m-%Y").strftime(
                        "%Y-%m-%d"
                    ),
                    "team1": row["team1"],
                    "team2": row["team2"],
                    "venue": row["venue"],
                }
                if Match.objects.filter(
                    date=match_data["date"],
                    team1=match_data["team1"],
                    team2=match_data["team2"],
                    venue=match_data["venue"],
                ).exists():
                    continue

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
                if TeamWinrates.objects.filter(
                    team=winrate_data["team"]
                ).exists():
                    continue
                
                serializer = WinratesSerializer(data=winrate_data)
                if serializer.is_valid():
                    serializer.save()
        matches = Match.objects.all()
        winrates = TeamWinrates.objects.all()
        matches_serializer = MatchSerializer(matches, many=True)
        winrates_serializer = WinratesSerializer(winrates, many=True)

        return Response(
            {"message": "Matches and win rates uploaded successfully!", "matches": matches_serializer.data, "winrates": winrates_serializer.data},
            status=status.HTTP_200_OK,
        )


class CurrentPredictionsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        today = date.today()
        matches = Match.objects.filter(date=today).distinct()

        if not matches.exists():
            return Response(
                {"message": "No matches scheduled for today."},
                status=status.HTTP_404_NOT_FOUND,
            )

        final_predictions = []

        for match in matches:
            team1 = match.team1
            team2 = match.team2
            venue = match.venue
            city = venue.split(",")[-1].strip()

            team1_win_rate = (
                TeamWinrates.objects.get(team=team1).home_win_percentage / 100
            )
            team2_win_rate = (
                TeamWinrates.objects.get(team=team2).away_win_percentage / 100
            )

            toss_outcomes = []

            scenarios = [
                {"toss_winner": team1, "toss_decision": "bat"},
                {"toss_winner": team1, "toss_decision": "field"},
                {"toss_winner": team2, "toss_decision": "bat"},
                {"toss_winner": team2, "toss_decision": "field"},
            ]

            for scenario in scenarios:
                result = predict_ipl_match(
                    team1=team1,
                    team2=team2,
                    venue=venue,
                    toss_winner=scenario["toss_winner"],
                    toss_decision=scenario["toss_decision"],
                    team1_win_rate=team1_win_rate,
                    team2_win_rate=team2_win_rate,
                )

                toss_outcomes.append(
                    {
                        "toss_winner": result["toss_winner"],
                        "toss_decision": result["toss_decision"],
                        "predicted_winner": result["predicted_winner"],
                        "winning_probability": result["winning_probability"],
                    }
                )

            match_prediction = {
                "team1": team1,
                "team2": team2,
                "venue": venue,
                "city": city,
                "team1_win_rate": team1_win_rate,
                "team2_win_rate": team2_win_rate,
                "team1_is_home": result.get("team1_is_home", 0),
                "team2_is_home": result.get("team2_is_home", 0),
                "team1_venue_win_pct": result.get("team1_venue_win_pct"),
                "team2_venue_win_pct": result.get("team2_venue_win_pct"),
                "toss_outcomes": toss_outcomes,
            }

            final_predictions.append(match_prediction)

        insights = analyze_predictions(final_predictions)

        return Response(
            {"predictions": final_predictions, "insights": insights},
            status=status.HTTP_200_OK,
        )


class ManualDatePredictionsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        selected_date = request.query_params.get("date")
        if not selected_date:
            return Response(
                {"error": "Please provide a date in the format YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        matches = Match.objects.filter(date=selected_date)

        if not matches.exists():
            return Response(
                {"message": f"No matches scheduled for {selected_date}."},
                status=status.HTTP_404_NOT_FOUND,
            )

        final_predictions = []

        for match in matches:
            team1 = match.team1
            team2 = match.team2
            venue = match.venue
            city = venue.split(",")[-1].strip()

            team1_win_rate = (
                TeamWinrates.objects.get(team=team1).home_win_percentage / 100
            )
            team2_win_rate = (
                TeamWinrates.objects.get(team=team2).away_win_percentage / 100
            )

            toss_outcomes = []

            scenarios = [
                {"toss_winner": team1, "toss_decision": "bat"},
                {"toss_winner": team1, "toss_decision": "field"},
                {"toss_winner": team2, "toss_decision": "bat"},
                {"toss_winner": team2, "toss_decision": "field"},
            ]

            for scenario in scenarios:
                result = predict_ipl_match(
                    team1=team1,
                    team2=team2,
                    venue=venue,
                    toss_winner=scenario["toss_winner"],
                    toss_decision=scenario["toss_decision"],
                    team1_win_rate=team1_win_rate,
                    team2_win_rate=team2_win_rate,
                )

                toss_outcomes.append(
                    {
                        "toss_winner": result["toss_winner"],
                        "toss_decision": result["toss_decision"],
                        "predicted_winner": result["predicted_winner"],
                        "winning_probability": result["winning_probability"],
                    }
                )

            match_prediction = {
                "team1": team1,
                "team2": team2,
                "venue": venue,
                "city": city,
                "team1_win_rate": team1_win_rate,
                "team2_win_rate": team2_win_rate,
                "team1_is_home": result.get("team1_is_home", 0),
                "team2_is_home": result.get("team2_is_home", 0),
                "team1_venue_win_pct": result.get("team1_venue_win_pct"),
                "team2_venue_win_pct": result.get("team2_venue_win_pct"),
                "toss_outcomes": toss_outcomes,
            }

            final_predictions.append(match_prediction)

        insights = analyze_predictions(final_predictions)

        return Response(
            {"predictions": final_predictions, "insights": insights},
            status=status.HTTP_200_OK,
        )